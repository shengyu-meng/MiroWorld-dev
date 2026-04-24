from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from threading import Lock, Thread
from typing import Any, Callable

from config import get_settings
from shared.utils import make_id, utc_now


ReasoningProgress = Callable[[str, str], None]
ReasoningWorker = Callable[[ReasoningProgress], dict[str, Any]]


@dataclass
class ReasoningArtifactTrailItem:
  step: str
  status: str
  summary: str
  artifact_path: str
  created_at: str

  def to_payload(self) -> dict[str, str]:
    return {
      "step": self.step,
      "status": self.status,
      "summary": self.summary,
      "artifact_path": self.artifact_path,
      "created_at": self.created_at,
    }


@dataclass
class ReasoningJob:
  job_id: str
  project_id: str
  operation: str
  provider: str
  model_name: str
  status: str
  progress_step: str
  summary: str
  running_summary: str
  artifact_group: str
  artifact_path: str | None
  created_at: str
  updated_at: str
  artifact_trail: list[ReasoningArtifactTrailItem] = field(default_factory=list)

  def to_payload(self) -> dict[str, Any]:
    return {
      "job_id": self.job_id,
      "project_id": self.project_id,
      "operation": self.operation,
      "provider": self.provider,
      "model_name": self.model_name,
      "status": self.status,
      "progress_step": self.progress_step,
      "summary": self.summary,
      "artifact_path": self.artifact_path,
      "artifact_trail": [item.to_payload() for item in self.artifact_trail],
      "updated_at": self.updated_at,
      "stage": None,
    }


class ReasoningJobManager:
  def __init__(self, *, provider: str, model_name: str) -> None:
    self.provider = provider
    self.model_name = model_name
    self.auto_start = True
    self._jobs: dict[str, ReasoningJob] = {}
    self._project_jobs: dict[str, str] = {}
    self._workers: dict[str, ReasoningWorker] = {}
    self._lock = Lock()

  def enqueue(
    self,
    project_id: str,
    worker: ReasoningWorker,
    *,
    operation: str = "seed_compiler",
    queued_summary: str = "MiniMax seed reasoning is queued as backstage computation.",
    running_summary: str = "MiniMax is building a structured public reasoning packet.",
    artifact_group: str = "reasoning",
  ) -> dict[str, Any]:
    with self._lock:
      existing = self._active_project_job(project_id)
      if existing:
        return existing.to_payload()

      now = utc_now()
      job = ReasoningJob(
        job_id=make_id("rjob"),
        project_id=project_id,
        operation=operation,
        provider=self.provider,
        model_name=self.model_name,
        status="queued",
        progress_step="queued",
        summary=queued_summary,
        running_summary=running_summary,
        artifact_group=artifact_group,
        artifact_path=None,
        created_at=now,
        updated_at=now,
      )
      job.artifact_path = self._record_artifact_locked(job)
      self._jobs[job.job_id] = job
      self._project_jobs[project_id] = job.job_id
      self._workers[job.job_id] = worker

    if self.auto_start:
      Thread(target=self._run_job, args=(job.job_id,), daemon=True).start()
    return job.to_payload()

  def get(self, project_id: str) -> dict[str, Any] | None:
    with self._lock:
      job_id = self._project_jobs.get(project_id)
      if not job_id:
        return None
      job = self._jobs.get(job_id)
      return job.to_payload() if job else None

  def run_queued_for_tests(self, project_id: str) -> dict[str, Any] | None:
    with self._lock:
      job_id = self._project_jobs.get(project_id)
    if not job_id:
      return None
    self._run_job(job_id)
    return self.get(project_id)

  def _active_project_job(self, project_id: str) -> ReasoningJob | None:
    job_id = self._project_jobs.get(project_id)
    if not job_id:
      return None
    job = self._jobs.get(job_id)
    if job and job.status in {"queued", "running"}:
      return job
    return None

  def _run_job(self, job_id: str) -> None:
    worker = self._workers.get(job_id)
    if not worker:
      return
    with self._lock:
      job = self._jobs.get(job_id)
      running_summary = job.running_summary if job else "MiniMax is building a structured public reasoning packet."
    self._update(
      job_id,
      status="running",
      progress_step="requesting_model",
      summary=running_summary,
    )
    try:
      result = worker(lambda step, summary: self._update(job_id, progress_step=step, summary=summary))
      status = str(result.get("status") or "completed")
      if status not in {"completed", "fallback", "failed"}:
        status = "completed"
      self._update(
        job_id,
        status=status,
        progress_step=str(result.get("progress_step") or status),
        summary=str(result.get("summary") or "MiniMax backstage reasoning finished."),
        artifact_path=result.get("artifact_path"),
      )
    except Exception as exc:
      self._update(
        job_id,
        status="failed",
        progress_step="failed",
        summary=f"{exc.__class__.__name__}: {str(exc)[:180]}",
      )
    finally:
      with self._lock:
        self._workers.pop(job_id, None)

  def _update(
    self,
    job_id: str,
    *,
    status: str | None = None,
    progress_step: str | None = None,
    summary: str | None = None,
    artifact_path: str | None = None,
  ) -> None:
    with self._lock:
      job = self._jobs.get(job_id)
      if not job:
        return
      if status:
        job.status = status
      if progress_step:
        job.progress_step = progress_step
      if summary:
        job.summary = summary
      if artifact_path:
        job.artifact_path = artifact_path
      job.updated_at = utc_now()
      if status or progress_step or summary:
        trail_path = self._record_artifact_locked(job)
        if not artifact_path:
          job.artifact_path = trail_path

  def _record_artifact_locked(self, job: ReasoningJob) -> str:
    created_at = utc_now()
    safe_step = re.sub(r"[^a-zA-Z0-9_-]+", "-", job.progress_step).strip("-") or "step"
    sequence = len(job.artifact_trail)
    relative_path = (
      f"data/runtime/process/{job.project_id}/{job.artifact_group}/"
      f"{job.job_id}/{sequence:02d}-{safe_step}.json"
    )
    absolute_path = (
      get_settings().data_dir
      / "process"
      / job.project_id
      / job.artifact_group
      / job.job_id
      / f"{sequence:02d}-{safe_step}.json"
    )
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
      "generated_at": created_at,
      "artifact_type": "miroworld_backstage_reasoning_checkpoint",
      "job_id": job.job_id,
      "project_id": job.project_id,
      "operation": job.operation,
      "provider": job.provider,
      "model_name": job.model_name,
      "status": job.status,
      "progress_step": job.progress_step,
      "summary": job.summary,
      "result_artifact_path": job.artifact_path,
      "note": "This checkpoint stores only public job progress metadata; no API key, seed prompt, raw provider hidden reasoning, or user secret is stored.",
    }
    absolute_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    job.artifact_trail.append(
      ReasoningArtifactTrailItem(
        step=job.progress_step,
        status=job.status,
        summary=job.summary,
        artifact_path=relative_path,
        created_at=created_at,
      )
    )
    return relative_path

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock, Thread
from typing import Any, Callable

from shared.utils import make_id, utc_now


ReasoningProgress = Callable[[str, str], None]
ReasoningWorker = Callable[[ReasoningProgress], dict[str, Any]]


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
  artifact_path: str | None
  created_at: str
  updated_at: str

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

  def enqueue(self, project_id: str, worker: ReasoningWorker) -> dict[str, Any]:
    with self._lock:
      existing = self._active_project_job(project_id)
      if existing:
        return existing.to_payload()

      now = utc_now()
      job = ReasoningJob(
        job_id=make_id("rjob"),
        project_id=project_id,
        operation="seed_compiler",
        provider=self.provider,
        model_name=self.model_name,
        status="queued",
        progress_step="queued",
        summary="MiniMax seed reasoning is queued as backstage computation.",
        artifact_path=None,
        created_at=now,
        updated_at=now,
      )
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
    self._update(
      job_id,
      status="running",
      progress_step="requesting_model",
      summary="MiniMax is building a structured public reasoning packet.",
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

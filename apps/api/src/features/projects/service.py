from __future__ import annotations

from core.errors import ValidationError
from shared.utils import make_id, utc_now
from .calibration_engine import CalibrationEngine
from .editorial_engine import EditorialEngine
from .fixture_repository import FixtureRepository
from .models import (
  CalibrationRequest,
  DecisionLogEntry,
  EditorialRequest,
  InputRequest,
  ProjectCreateRequest,
  ProjectSnapshot,
  ReplaySetSaveRequest,
  ReplayTraceItem,
  SavedReplaySet,
  ShareRequest,
  TheatreProgress,
  TheatreProgressRequest,
  UserInputRecord,
  WorldState,
)
from .repository import ProjectRepository
from .reasoning_jobs import ReasoningJobManager
from .replay_engine import ReplayEngine
from .seed_compiler import SeedCompiler
from .share_engine import ShareEngine
from .stage_builder import StageBuilder


class ProjectService:
  EFFECT_SCOPE_RULES = {
    "observation": {"evidence"},
    "correction": {"evidence", "world_state"},
    "intervention": {"world_state"},
    "preference": {"ranking"},
  }

  def __init__(self) -> None:
    self.fixture_repository = FixtureRepository()
    self.project_repository = ProjectRepository()
    self.seed_compiler = SeedCompiler()
    self.reasoning_jobs = ReasoningJobManager(
      provider="MiniMax",
      model_name=self.seed_compiler.llm_adapter.settings.llm_model_name,
    )
    self.editorial_jobs = ReasoningJobManager(
      provider="MiniMax",
      model_name=self.seed_compiler.llm_adapter.settings.llm_model_name,
    )
    self.editorial_engine = EditorialEngine(self.seed_compiler.llm_adapter)
    self.replay_engine = ReplayEngine()
    self.share_engine = ShareEngine()
    self.stage_builder = StageBuilder()
    self.calibration_engine = CalibrationEngine()

  def list_fixtures(self) -> dict:
    return self.fixture_repository.list_fixtures()

  def create_project(self, payload: ProjectCreateRequest) -> tuple[ProjectSnapshot, dict | None]:
    if not payload.fixture_id and not payload.seed_prompt:
      raise ValidationError("Either fixture_id or seed_prompt is required.")
    if payload.fixture_id and payload.seed_prompt:
      raise ValidationError("Use either fixture_id or seed_prompt, not both.")

    if payload.fixture_id:
      snapshot = self.seed_compiler.compile_fixture(
        self.fixture_repository.get_fixture(payload.fixture_id),
        payload.language,
      )
      return self.project_repository.save(snapshot), None
    else:
      snapshot = self.seed_compiler.compile_prompt(payload.seed_prompt or "", payload.language, use_llm=False)
      saved = self.project_repository.save(snapshot)
      reasoning = self._enqueue_prompt_reasoning(saved, payload.seed_prompt or "", payload.language)
      return saved, reasoning

  def get_stage(self, project_id: str, language: str) -> dict:
    snapshot = self.project_repository.load(project_id)
    snapshot.project.language = language
    snapshot.world_state.share_artifact = self.share_engine.build(snapshot.world_state, language)
    self.project_repository.save(snapshot)
    return self.stage_builder.build(snapshot.world_state, language)

  def get_reasoning_status(self, project_id: str, language: str) -> dict:
    job = self.reasoning_jobs.get(project_id)
    if job:
      if job["status"] in {"completed", "fallback", "failed"}:
        job["stage"] = self.get_stage(project_id, language)
      return job

    snapshot = self.project_repository.load(project_id)
    latest_run = snapshot.world_state.reasoning_runs[-1] if snapshot.world_state.reasoning_runs else None
    if latest_run:
      return {
        "job_id": latest_run.reasoning_run_id,
        "project_id": project_id,
        "operation": latest_run.operation,
        "provider": latest_run.provider,
        "model_name": latest_run.model_name,
        "status": latest_run.status,
        "progress_step": latest_run.status,
        "summary": latest_run.summary,
        "artifact_path": latest_run.artifact_path,
        "artifact_trail": [],
        "updated_at": latest_run.created_at,
        "stage": self.get_stage(project_id, language),
      }

    settings = self.seed_compiler.llm_adapter.settings
    is_prompt = snapshot.project.source_mode == "seed_prompt"
    disabled = not is_prompt or not settings.llm_seed_compiler_enabled or not settings.llm_api_key
    return {
      "job_id": "",
      "project_id": project_id,
      "operation": "seed_compiler",
      "provider": "MiniMax",
      "model_name": settings.llm_model_name,
      "status": "disabled" if disabled else "idle",
      "progress_step": "not_started",
      "summary": "MiniMax backstage reasoning is not active for this project.",
      "artifact_path": None,
      "artifact_trail": [],
      "updated_at": snapshot.world_state.updated_at,
      "stage": None,
    }

  def request_editorial_takeaway(self, project_id: str, payload: EditorialRequest) -> dict:
    # Validate the project before accepting a background job.
    self.project_repository.load(project_id)

    def worker(progress):
      latest = self.project_repository.load(project_id)
      return self.editorial_engine.run_takeaway(latest, payload.language, progress)

    job = self.editorial_jobs.enqueue(
      project_id,
      worker,
      operation="editorial_takeaway",
      queued_summary="Editorial takeaway is queued as a safe backstage artifact.",
      running_summary="MiniMax is drafting a public editorial takeaway.",
      artifact_group="editorial",
    )
    return self._decorate_editorial_status(job)

  def get_editorial_status(self, project_id: str, language: str) -> dict:
    job = self.editorial_jobs.get(project_id)
    if job:
      return self._decorate_editorial_status(job)

    snapshot = self.project_repository.load(project_id)
    settings = self.seed_compiler.llm_adapter.settings
    return {
      "job_id": "",
      "project_id": project_id,
      "operation": "editorial_takeaway",
      "provider": "MiniMax",
      "model_name": settings.llm_model_name,
      "status": "idle",
      "progress_step": "not_started",
      "summary": "Editorial takeaway lane is ready; request it from Archive when the worldline has enough afterimage.",
      "artifact_path": None,
      "artifact_trail": [],
      "updated_at": snapshot.world_state.updated_at,
      "editorial": None,
    }

  def apply_input(self, project_id: str, payload: InputRequest) -> tuple[dict, object | None]:
    self._validate_effect_scope(payload.input_type, payload.effect_scope)
    snapshot = self.project_repository.load(project_id)
    input_record = UserInputRecord(
      input_id=make_id("input"),
      input_type=payload.input_type,
      content=payload.content.strip(),
      target_event_id=payload.target_event_id,
      target_branch_id=payload.target_branch_id,
      effect_scope=payload.effect_scope,
      created_at=utc_now(),
    )
    snapshot.world_state.player_inputs.insert(0, input_record)
    replay_result = self.replay_engine.maybe_replay(snapshot.world_state, payload)
    if replay_result is None:
      self.replay_engine.cost_confidence_engine.apply(snapshot.world_state, payload)
    snapshot.world_state.player_decision_log.insert(
      0,
      DecisionLogEntry(
        entry_id=make_id("log"),
        created_at=utc_now(),
        input_type=payload.input_type,
        event_id=payload.target_event_id,
        event_title=self._lookup_event_title(snapshot, payload.target_event_id),
        branch_id=payload.target_branch_id,
        branch_label=self._lookup_branch_label(snapshot, payload.target_branch_id),
        content=payload.content.strip(),
        replay_summary=replay_result.summary if replay_result else self._build_non_replay_summary(payload.language, payload.input_type),
        cost_changes=replay_result.cost_changes if replay_result else [],
      ),
    )
    snapshot.world_state.share_artifact = self.share_engine.build(snapshot.world_state, payload.language)
    snapshot.world_state.updated_at = utc_now()
    self.project_repository.save(snapshot)
    return self.stage_builder.build(snapshot.world_state, payload.language), replay_result

  def build_share(self, project_id: str, payload: ShareRequest) -> dict:
    snapshot = self.project_repository.load(project_id)
    artifact = self.share_engine.build(
      snapshot.world_state,
      payload.language,
      event_id=payload.event_id,
      branch_id=payload.branch_id,
    )
    snapshot.world_state.share_artifact = artifact
    snapshot.world_state.updated_at = utc_now()
    self.project_repository.save(snapshot)
    return artifact.model_dump(mode="json")

  def record_calibration(self, project_id: str, payload: CalibrationRequest) -> dict:
    snapshot = self.project_repository.load(project_id)
    self.calibration_engine.record(snapshot.world_state, payload)
    snapshot.world_state.updated_at = utc_now()
    self.project_repository.save(snapshot)
    return self.stage_builder.build(snapshot.world_state, payload.language)

  def save_theatre_progress(self, project_id: str, payload: TheatreProgressRequest) -> dict:
    snapshot = self.project_repository.load(project_id)
    snapshot.project.language = payload.language
    progress = self._sanitize_theatre_progress(snapshot.world_state, payload)
    snapshot.world_state.theatre_progress = progress
    snapshot.world_state.updated_at = progress.updated_at
    snapshot.project.updated_at = progress.updated_at
    self.project_repository.save(snapshot)
    return progress.model_dump(mode="json")

  def save_replay_set(self, project_id: str, payload: ReplaySetSaveRequest) -> list[dict]:
    snapshot = self.project_repository.load(project_id)
    saved_replay = SavedReplaySet(
      replay_set_id=make_id("rset"),
      saved_at=utc_now(),
      **payload.model_dump(mode="python"),
    )
    snapshot.world_state.saved_replay_sets = [
      saved_replay,
      *[
        item
        for item in snapshot.world_state.saved_replay_sets
        if not self._is_same_saved_replay(item, payload)
      ],
    ][:8]
    snapshot.world_state.updated_at = utc_now()
    self.project_repository.save(snapshot)
    return [item.model_dump(mode="json") for item in snapshot.world_state.saved_replay_sets]

  def delete_replay_set(self, project_id: str, replay_set_id: str) -> list[dict]:
    snapshot = self.project_repository.load(project_id)
    snapshot.world_state.saved_replay_sets = [
      item
      for item in snapshot.world_state.saved_replay_sets
      if item.replay_set_id != replay_set_id
    ]
    snapshot.world_state.updated_at = utc_now()
    self.project_repository.save(snapshot)
    return [item.model_dump(mode="json") for item in snapshot.world_state.saved_replay_sets]

  def _enqueue_prompt_reasoning(self, snapshot: ProjectSnapshot, seed_prompt: str, language: str) -> dict | None:
    settings = self.seed_compiler.llm_adapter.settings
    if not settings.llm_seed_compiler_enabled or not settings.llm_api_key:
      return None

    project_id = snapshot.project.project_id

    def worker(progress):
      return self._run_prompt_reasoning(project_id, seed_prompt, language, progress)

    return self.reasoning_jobs.enqueue(project_id, worker)

  def _run_prompt_reasoning(self, project_id: str, seed_prompt: str, language: str, progress) -> dict:
    progress("requesting_model", "MiniMax is compiling a structured public worldline packet.")
    latest = self.project_repository.load(project_id)
    enriched = self.seed_compiler.compile_prompt(
      seed_prompt,
      language,  # type: ignore[arg-type]
      use_llm=True,
      project_id=latest.project.project_id,
      world_state_id=latest.world_state.world_state_id,
      session_id=latest.world_state.session_id,
    )
    run = enriched.world_state.reasoning_runs[-1] if enriched.world_state.reasoning_runs else None
    progress("merging_worldline", "Merging MiniMax packet into the project snapshot.")
    merged = self._merge_reasoning_snapshot(latest, enriched)
    self.project_repository.save(merged)
    if not run:
      return {
        "status": "failed",
        "progress_step": "no_reasoning_run",
        "summary": "MiniMax did not produce a reasoning run record.",
        "artifact_path": None,
      }
    return {
      "status": run.status,
      "progress_step": "merged" if run.status == "completed" else run.status,
      "summary": run.summary,
      "artifact_path": run.artifact_path,
    }

  def _merge_reasoning_snapshot(self, current: ProjectSnapshot, enriched: ProjectSnapshot) -> ProjectSnapshot:
    has_viewer_authored_state = any([
      current.world_state.player_inputs,
      current.world_state.player_decision_log,
      current.world_state.calibration_records,
      current.world_state.saved_replay_sets,
    ])
    if has_viewer_authored_state:
      current.world_state.reasoning_runs = self._merge_reasoning_runs(
        current.world_state.reasoning_runs,
        enriched.world_state.reasoning_runs,
      )
      current.world_state.updated_at = utc_now()
      current.project.updated_at = current.world_state.updated_at
      return current

    progress = self._map_progress_to_enriched_worldline(current, enriched)
    enriched.project.created_at = current.project.created_at
    enriched.project.updated_at = utc_now()
    enriched.world_state.created_at = current.world_state.created_at
    enriched.world_state.updated_at = enriched.project.updated_at
    enriched.world_state.theatre_progress = progress
    enriched.world_state.player_inputs = current.world_state.player_inputs
    enriched.world_state.player_decision_log = current.world_state.player_decision_log
    enriched.world_state.calibration_records = current.world_state.calibration_records
    enriched.world_state.saved_replay_sets = current.world_state.saved_replay_sets
    return enriched

  def _merge_reasoning_runs(self, current_runs, next_runs):
    seen = {run.reasoning_run_id for run in current_runs}
    return [
      *current_runs,
      *[run for run in next_runs if run.reasoning_run_id not in seen],
    ]

  def _map_progress_to_enriched_worldline(self, current: ProjectSnapshot, enriched: ProjectSnapshot) -> TheatreProgress:
    current_progress = current.world_state.theatre_progress
    current_events = current.world_state.key_events
    selected_index = next(
      (index for index, event in enumerate(current_events) if event.event_id == current_progress.selected_event_id),
      0,
    )
    next_events = enriched.world_state.key_events
    next_index = min(selected_index, max(0, len(next_events) - 1))
    next_event = next_events[next_index] if next_events else None
    next_branch = (
      next((branch for branch in next_event.branches if branch.visibility == "primary"), next_event.branches[0])
      if next_event and next_event.branches
      else None
    )
    return TheatreProgress(
      revealed_event_count=max(1, min(current_progress.revealed_event_count, len(next_events) or 1)),
      selected_event_id=next_event.event_id if next_event else "",
      selected_branch_id=next_branch.branch_id if next_branch else "",
      active_surface=current_progress.active_surface,
      updated_at=utc_now(),
    )

  def _validate_effect_scope(self, input_type: str, effect_scope: str) -> None:
    allowed = self.EFFECT_SCOPE_RULES[input_type]
    if effect_scope not in allowed:
      raise ValidationError(
        f"effect_scope '{effect_scope}' is not allowed for input_type '{input_type}'.",
        details={"allowed": sorted(allowed)},
      )

  def _lookup_event_title(self, snapshot: ProjectSnapshot, event_id: str) -> str:
    for event in snapshot.world_state.key_events:
      if event.event_id == event_id:
        return event.title
    return ""

  def _lookup_branch_label(self, snapshot: ProjectSnapshot, branch_id: str) -> str:
    for event in snapshot.world_state.key_events:
      for branch in event.branches:
        if branch.branch_id == branch_id:
          return branch.label
    return ""

  def _sanitize_theatre_progress(self, world_state: WorldState, payload: TheatreProgressRequest) -> TheatreProgress:
    if not world_state.key_events:
      raise ValidationError("Cannot save theatre progress without key events.")

    selected_event = next(
      (event for event in world_state.key_events if event.event_id == payload.selected_event_id),
      world_state.key_events[0],
    )
    if not selected_event.branches:
      raise ValidationError("Cannot save theatre progress for an event without branches.")

    selected_branch = next(
      (branch for branch in selected_event.branches if branch.branch_id == payload.selected_branch_id),
      next((branch for branch in selected_event.branches if branch.visibility == "primary"), selected_event.branches[0]),
    )
    selected_index = world_state.key_events.index(selected_event)
    revealed_event_count = max(
      1,
      min(
        len(world_state.key_events),
        max(payload.revealed_event_count, selected_index + 1),
      ),
    )
    return TheatreProgress(
      revealed_event_count=revealed_event_count,
      selected_event_id=selected_event.event_id,
      selected_branch_id=selected_branch.branch_id,
      active_surface=payload.active_surface,
      updated_at=utc_now(),
    )

  def _is_same_saved_replay(self, saved_replay: SavedReplaySet, payload: ReplaySetSaveRequest) -> bool:
    return (
      saved_replay.replay_set_key == payload.replay_set_key
      and saved_replay.replay_set_label == payload.replay_set_label
      and saved_replay.focus.event_id == payload.focus.event_id
      and saved_replay.focus.branch_id == payload.focus.branch_id
    )

  def _decorate_editorial_status(self, job: dict) -> dict:
    return {
      **job,
      "editorial": self.editorial_engine.read_takeaway_artifact(job.get("artifact_path")),
    }

  def _build_non_replay_summary(self, language: str, input_type: str) -> str:
    if language == "zh":
      return f"{input_type} 更新了当前分支的可见度与排序。"
    return f"The {input_type} updated the visibility and ranking of the current branch."

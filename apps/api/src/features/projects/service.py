from __future__ import annotations

from core.errors import ValidationError
from shared.utils import make_id, utc_now
from .calibration_engine import CalibrationEngine
from .fixture_repository import FixtureRepository
from .models import (
  CalibrationRequest,
  DecisionLogEntry,
  InputRequest,
  ProjectCreateRequest,
  ProjectSnapshot,
  ReplayTraceItem,
  ShareRequest,
  UserInputRecord,
)
from .repository import ProjectRepository
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
    self.replay_engine = ReplayEngine()
    self.share_engine = ShareEngine()
    self.stage_builder = StageBuilder()
    self.calibration_engine = CalibrationEngine()

  def list_fixtures(self) -> dict:
    return self.fixture_repository.list_fixtures()

  def create_project(self, payload: ProjectCreateRequest) -> ProjectSnapshot:
    if not payload.fixture_id and not payload.seed_prompt:
      raise ValidationError("Either fixture_id or seed_prompt is required.")
    if payload.fixture_id and payload.seed_prompt:
      raise ValidationError("Use either fixture_id or seed_prompt, not both.")

    if payload.fixture_id:
      snapshot = self.seed_compiler.compile_fixture(
        self.fixture_repository.get_fixture(payload.fixture_id),
        payload.language,
      )
    else:
      snapshot = self.seed_compiler.compile_prompt(payload.seed_prompt or "", payload.language)
    return self.project_repository.save(snapshot)

  def get_stage(self, project_id: str, language: str) -> dict:
    snapshot = self.project_repository.load(project_id)
    snapshot.project.language = language
    snapshot.world_state.share_artifact = self.share_engine.build(snapshot.world_state, language)
    self.project_repository.save(snapshot)
    return self.stage_builder.build(snapshot.world_state, language)

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

  def _build_non_replay_summary(self, language: str, input_type: str) -> str:
    if language == "zh":
      return f"{input_type} 更新了当前分支的可见度与排序。"
    return f"The {input_type} updated the visibility and ranking of the current branch."

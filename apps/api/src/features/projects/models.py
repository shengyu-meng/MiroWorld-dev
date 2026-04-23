from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


DisplayLanguage = Literal["zh", "en"]
KnowledgeLayer = Literal["FACT", "INFERENCE", "VALUE", "ACTION"]
InputType = Literal["observation", "correction", "intervention", "preference"]
EffectScope = Literal["evidence", "world_state", "ranking"]
BranchVisibility = Literal["primary", "alternate"]
BranchState = Literal["candidate", "selected", "replayed", "invalidated"]
CalibrationResultType = Literal["hit", "partial", "miss", "insufficient_data"]


class SourceEntity(BaseModel):
  entity_id: str
  entity_kind: Literal["agent", "system", "constraint", "environment"]
  name: str
  description: str = ""


class KnowledgeItem(BaseModel):
  id: str
  layer: KnowledgeLayer
  content: str
  source_type: str
  source_ref: str | None = None
  confidence: float = Field(ge=0, le=1)


class ConfidenceUpdate(BaseModel):
  update_id: str
  target_type: Literal["event", "branch"]
  target_id: str
  before: float = Field(ge=0, le=1)
  after: float = Field(ge=0, le=1)
  reason: str
  method: str
  created_at: str


class Branch(BaseModel):
  branch_id: str
  event_id: str
  label: str
  description: str
  confidence: float = Field(ge=0, le=1)
  premises: list[str]
  signals_for: list[str]
  signals_against: list[str]
  visibility: BranchVisibility
  state: BranchState
  cost_hint: str = ""
  player_memory_count: int = 0
  player_memory_note: str = ""
  memory_confidence_delta: float = 0
  effective_confidence: float | None = None
  player_influence: Literal["reinforced", "contested", "pressured", "neutral"] = "neutral"


class KeyEvent(BaseModel):
  event_id: str
  world_state_id: str
  title: str
  summary: str
  depends_on_event_id: str = ""
  causal_note: str = ""
  causal_strength: Literal["low", "medium", "high"] = "medium"
  collapse_hint: str = ""
  stage: str
  impact_level: Literal["low", "medium", "high"] = "medium"
  fold_state: Literal["collapsed", "expanded"] = "collapsed"
  branches: list[Branch]
  evidence_ids: list[str]
  evidence_notes: list[str] = Field(default_factory=list)
  affected_entities: list[str] = Field(default_factory=list)


class CostLens(BaseModel):
  cost_lens_id: str
  target_branch_id: str
  first_order_costs: list[str]
  second_order_costs: list[str]
  affected_groups: list[str]
  ethical_notes: list[str]


class ReplayResult(BaseModel):
  replay_id: str
  checkpoint_id: str
  before_branch_id: str
  after_branch_id: str
  input_style: InputType
  impact_mode: Literal["visibility_shift", "premise_rewrite", "worldline_write", "value_reweight"]
  changed_events: list[str]
  changed_branches: list[str]
  cost_changes: list[str]
  summary: str


class ShareArtifact(BaseModel):
  title: str
  subtitle: str
  summary: str
  disclaimer: str
  share_text: str
  tags: list[str]
  short_excerpt: str = ""
  poster_caption: str = ""
  curator_note: str = ""
  wall_label: str = ""
  archive_summary: str = ""


class UserInputRecord(BaseModel):
  input_id: str
  input_type: InputType
  content: str
  target_event_id: str
  target_branch_id: str
  effect_scope: EffectScope
  created_at: str


class CalibrationRecord(BaseModel):
  calibration_id: str
  event_id: str
  branch_id: str
  result: CalibrationResultType
  actual_outcome: str
  note: str = ""
  created_at: str


class DecisionLogEntry(BaseModel):
  entry_id: str
  created_at: str
  input_type: InputType
  event_id: str
  event_title: str
  branch_id: str
  branch_label: str
  content: str
  replay_summary: str
  cost_changes: list[str] = Field(default_factory=list)


class ReplayTraceItem(BaseModel):
  trace_id: str
  event_id: str
  event_title: str
  branch_id: str
  branch_label: str
  summary: str


class SavedReplayFocus(BaseModel):
  event_id: str
  event_title: str
  branch_id: str
  branch_label: str


class SavedReplayDossierCard(BaseModel):
  title: str
  summary: str


class SavedReplayDossier(BaseModel):
  summary: str
  entry: SavedReplayDossierCard
  hinge: SavedReplayDossierCard
  terminal: SavedReplayDossierCard


class SavedReplayArtifact(BaseModel):
  title: str
  deck: str
  wall_text: str
  pressure_note: str
  closing_note: str
  tags: list[str]


class SavedReplayMetrics(BaseModel):
  event_count: int
  average_confidence: float
  average_pressure: float
  alternate_count: int


class SavedReplayTimelineEntry(BaseModel):
  index: str
  stage: str
  event_title: str
  branch_label: str
  confidence: float
  counter_signal_count: int
  description: str
  upstream: SavedReplayDossierCard
  downstream: SavedReplayDossierCard
  focus: SavedReplayFocus


class SavedReplaySetDraft(BaseModel):
  replay_set_key: str
  replay_set_label: str
  replay_set_note: str
  authored_note: str
  artifact: SavedReplayArtifact
  focus: SavedReplayFocus
  metrics: SavedReplayMetrics
  dossier: SavedReplayDossier
  timeline: list[SavedReplayTimelineEntry]
  language: DisplayLanguage = "zh"


class SavedReplaySet(SavedReplaySetDraft):
  replay_set_id: str
  saved_at: str


class ProjectRecord(BaseModel):
  project_id: str
  title: str
  source_mode: Literal["fixture", "seed_prompt"]
  source_label: str
  seed_prompt: str = ""
  created_at: str
  updated_at: str
  language: DisplayLanguage = "zh"


class WorldState(BaseModel):
  world_state_id: str
  project_id: str
  session_id: str
  version: int = Field(ge=1)
  status: Literal["draft", "active", "replayed", "reviewed"] = "active"
  headline: str
  summary: str
  source_mode: Literal["fixture", "project_graph", "simulation_timeline", "v2_branch_kernel"] = "fixture"
  source_label: str
  disclaimer: str
  share_context: str
  share_artifact: ShareArtifact
  entities: list[SourceEntity]
  key_events: list[KeyEvent]
  cost_lenses: list[CostLens]
  knowledge_items: list[KnowledgeItem] = Field(default_factory=list)
  confidence_updates: list[ConfidenceUpdate] = Field(default_factory=list)
  player_inputs: list[UserInputRecord] = Field(default_factory=list)
  player_decision_log: list[DecisionLogEntry] = Field(default_factory=list)
  replay_trace: list[ReplayTraceItem] = Field(default_factory=list)
  saved_replay_sets: list[SavedReplaySet] = Field(default_factory=list)
  calibration_records: list[CalibrationRecord] = Field(default_factory=list)
  created_at: str
  updated_at: str


class ProjectSnapshot(BaseModel):
  project: ProjectRecord
  world_state: WorldState


class ProjectCreateRequest(BaseModel):
  fixture_id: str | None = None
  seed_prompt: str | None = None
  language: DisplayLanguage = "zh"


class ProjectCreateResponse(BaseModel):
  project_id: str
  stage: dict


class InputRequest(BaseModel):
  input_type: InputType
  content: str
  target_event_id: str
  target_branch_id: str
  effect_scope: EffectScope
  language: DisplayLanguage = "zh"


class InputResponse(BaseModel):
  stage: dict
  replay_result: ReplayResult | None = None


class ShareRequest(BaseModel):
  language: DisplayLanguage = "zh"
  event_id: str | None = None
  branch_id: str | None = None


class CalibrationRequest(BaseModel):
  event_id: str
  branch_id: str
  result: CalibrationResultType
  actual_outcome: str
  note: str = ""
  language: DisplayLanguage = "zh"


class ReplaySetSaveRequest(SavedReplaySetDraft):
  pass

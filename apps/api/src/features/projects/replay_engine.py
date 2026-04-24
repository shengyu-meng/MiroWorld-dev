from __future__ import annotations

from shared.utils import make_id
from .cost_confidence_engine import CostConfidenceEngine
from .models import InputRequest, ReplayResult, ReplayTraceItem, WorldState


class ReplayEngine:
  def __init__(self) -> None:
    self.cost_confidence_engine = CostConfidenceEngine()

  def maybe_replay(self, world_state: WorldState, payload: InputRequest) -> ReplayResult | None:
    if payload.input_type not in {"correction", "intervention"}:
      return None
    changed_events, changed_branches, impact_mode = self.cost_confidence_engine.apply(world_state, payload)
    world_state.version += 1
    world_state.status = "replayed"
    world_state.replay_trace.insert(
      0,
      ReplayTraceItem(
        trace_id=make_id("rt"),
        event_id=payload.target_event_id,
        event_title=self._lookup_event_title(world_state, payload.target_event_id),
        branch_id=payload.target_branch_id,
        branch_label=self._lookup_branch_label(world_state, payload.target_branch_id),
        summary=self._build_summary(payload),
      ),
    )
    return ReplayResult(
      replay_id=make_id("rp"),
      checkpoint_id=payload.target_event_id,
      before_branch_id=payload.target_branch_id,
      after_branch_id=payload.target_branch_id,
      input_style=payload.input_type,
      impact_mode=impact_mode,
      changed_events=changed_events,
      changed_branches=changed_branches,
      cost_changes=[
        "resource pressure rerouted",
        "field pressure redistributed",
      ],
      summary=self._build_summary(payload),
    )

  def _lookup_event_title(self, world_state: WorldState, event_id: str) -> str:
    for event in world_state.key_events:
      if event.event_id == event_id:
        return event.title
    return ""

  def _lookup_branch_label(self, world_state: WorldState, branch_id: str) -> str:
    for event in world_state.key_events:
      for branch in event.branches:
        if branch.branch_id == branch_id:
          return branch.label
    return ""

  def _build_summary(self, payload: InputRequest) -> str:
    if payload.language == "zh":
      return f"{payload.input_type} 从检查点之后改写了世界线的后续弯折。"
    return f"The {payload.input_type} rewrote the downstream bend of the worldline after the checkpoint."

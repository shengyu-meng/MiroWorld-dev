from __future__ import annotations

from shared.utils import clamp, make_id, utc_now
from .models import ConfidenceUpdate, InputRequest, KeyEvent, WorldState


class CostConfidenceEngine:
  EFFECT_RULES = {
    "observation": ("visibility_shift", 0.03),
    "correction": ("premise_rewrite", 0.08),
    "intervention": ("worldline_write", 0.12),
    "preference": ("value_reweight", 0.05),
  }

  def apply(self, world_state: WorldState, payload: InputRequest) -> tuple[list[str], list[str], str]:
    impact_mode, delta = self.EFFECT_RULES[payload.input_type]
    changed_events: list[str] = []
    changed_branches: list[str] = []

    for event in world_state.key_events:
      if event.event_id != payload.target_event_id:
        continue
      changed_events.append(event.event_id)
      for branch in event.branches:
        if branch.branch_id == payload.target_branch_id:
          before = branch.confidence
          direction = 1 if payload.input_type != "preference" else 0.5
          branch.confidence = clamp(branch.confidence + delta * direction)
          branch.effective_confidence = branch.confidence
          branch.player_memory_count += 1
          branch.player_influence = "pressured" if payload.input_type == "intervention" else "reinforced"
          branch.memory_confidence_delta = round(branch.confidence - before, 3)
          branch.state = "replayed" if payload.input_type in {"correction", "intervention"} else branch.state
          changed_branches.append(branch.branch_id)
          world_state.confidence_updates.append(
            ConfidenceUpdate(
              update_id=make_id("cu"),
              target_type="branch",
              target_id=branch.branch_id,
              before=before,
              after=branch.confidence,
              reason=f"{payload.input_type}:{payload.effect_scope}",
              method="rule",
              created_at=utc_now(),
            )
          )
        else:
          branch.confidence = clamp(branch.confidence - (delta / 2))
          branch.effective_confidence = branch.confidence
    return changed_events, changed_branches, impact_mode

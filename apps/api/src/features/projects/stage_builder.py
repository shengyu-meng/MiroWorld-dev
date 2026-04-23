from __future__ import annotations

from .models import Branch, DisplayLanguage, KeyEvent, ShareArtifact, WorldState


class StageBuilder:
  def build(self, world_state: WorldState, language: DisplayLanguage) -> dict:
    selected_event = world_state.key_events[0]
    selected_branch = selected_event.branches[0]
    calibration_summary = self._build_calibration_summary(world_state, language)
    return {
      "project_context": {
        "project_id": world_state.project_id,
        "headline": world_state.headline,
        "summary": world_state.summary,
        "status": world_state.status,
        "source_label": world_state.source_label,
        "display_language": language,
      },
      "surface_defaults": {
        "selected_event_id": selected_event.event_id,
        "selected_branch_id": selected_branch.branch_id,
        "active_surface": "observatory",
      },
      "observatory": {
        "knowledge_layers": ["FACT", "INFERENCE", "VALUE", "ACTION"],
        "key_events": [self._event_to_stage(event) for event in world_state.key_events],
        "worldline_track": [
          {
            "event_id": event.event_id,
            "title": event.title,
            "stage": event.stage,
            "primary_branch_id": event.branches[0].branch_id,
            "primary_branch_label": event.branches[0].label,
            "confidence": event.branches[0].confidence,
          }
          for event in world_state.key_events
        ],
      },
      "intervention": {
        "available_input_types": ["observation", "correction", "intervention", "preference"],
        "selected_branch_cards": [
          {
            "label": selected_branch.label,
            "description": selected_branch.description,
            "premises": selected_branch.premises,
            "signals_for": selected_branch.signals_for,
            "signals_against": selected_branch.signals_against,
          }
        ],
      },
      "cost_lens": {
        "lenses": [lens.model_dump(mode="json") for lens in world_state.cost_lenses],
        "passive_floor": {
          "title": "passive floor",
          "summary": self._translate(
            language,
            "就算你不介入，代价也已经在向不同群体滑移。",
            "Even without intervention, the cost is already sliding toward different groups.",
          ),
        },
      },
      "ripple": {
        "latest_bend": world_state.replay_trace[0].summary if world_state.replay_trace else "",
        "ripple_cards": [
          {
            "title": item.event_title,
            "summary": item.summary,
            "branch_label": item.branch_label,
          }
          for item in world_state.replay_trace[:5]
        ],
      },
      "archive": {
        "share_snapshot": world_state.share_artifact.model_dump(mode="json"),
        "player_decision_log": [entry.model_dump(mode="json") for entry in world_state.player_decision_log[:12]],
        "calibration_records": [record.model_dump(mode="json") for record in world_state.calibration_records[:12]],
        "calibration_summary": calibration_summary,
      },
      "version": world_state.version,
    }

  def _event_to_stage(self, event: KeyEvent) -> dict:
    return {
      "event_id": event.event_id,
      "title": event.title,
      "summary": event.summary,
      "stage": event.stage,
      "impact_level": event.impact_level,
      "affected_entities": event.affected_entities,
      "evidence_notes": event.evidence_notes,
      "branches": [branch.model_dump(mode="json") for branch in event.branches],
    }

  def _build_calibration_summary(self, world_state: WorldState, language: DisplayLanguage) -> dict:
    count = len(world_state.calibration_records)
    if language == "zh":
      summary = "还没有真实结果写入档案。" if count == 0 else f"已写入 {count} 条 calibration 记录。"
    else:
      summary = "No actual outcomes have been written into the archive yet." if count == 0 else f"{count} calibration records have been written into the archive."
    return {
      "count": count,
      "summary": summary,
    }

  def _translate(self, language: DisplayLanguage, zh: str, en: str) -> str:
    return zh if language == "zh" else en

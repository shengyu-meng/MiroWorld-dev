from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import get_settings
from shared.utils import make_id, utc_now
from .llm_adapter import OpenAICompatibleLLMAdapter
from .models import DisplayLanguage, ProjectSnapshot


class EditorialEngine:
  def __init__(self, llm_adapter: OpenAICompatibleLLMAdapter) -> None:
    self.llm_adapter = llm_adapter

  def run_takeaway(self, snapshot: ProjectSnapshot, language: DisplayLanguage, progress) -> dict[str, Any]:
    progress("building_context", "Collecting public Archive, Ripple, and calibration context.")
    context = self._build_context(snapshot, language)
    fallback = self._fallback_takeaway(context, language)

    if not self.llm_adapter.settings.llm_api_key:
      return self._write_result(
        snapshot,
        language,
        context,
        fallback,
        status="fallback",
        source="local_fallback",
        summary="MiniMax credentials are not configured; local editorial fallback is ready.",
      )

    progress("requesting_model", "MiniMax is drafting a public editorial takeaway from visible worldline artifacts.")
    packet = self.llm_adapter.generate_json(
      operation="editorial_takeaway",
      language=language,
      payload={
        "task": (
          "Create a concise public-facing editorial takeaway for MiroWorld. "
          "Use only the supplied public worldline context. Do not expose hidden reasoning, API keys, or private chain-of-thought."
        ),
        "language": language,
        "required_json_shape": {
          "title": "string",
          "summary": "string",
          "takeaways": ["string", "string", "string"],
          "ripple_note": "string",
          "calibration_note": "string",
          "intervention_note": "string",
          "disclaimer": "string",
        },
        "context": context,
      },
    )

    normalized = self._normalize_packet(packet, fallback)
    if normalized is None:
      progress("fallback", "MiniMax editorial output was unavailable or malformed; writing deterministic fallback.")
      return self._write_result(
        snapshot,
        language,
        context,
        fallback,
        status="fallback",
        source="local_fallback",
        summary=self._fallback_summary(),
      )

    progress("writing_artifact", "Writing safe editorial takeaway artifact.")
    return self._write_result(
      snapshot,
      language,
      context,
      normalized,
      status="completed",
      source="minimax",
      summary="MiniMax editorial takeaway is ready as a safe public artifact.",
    )

  def read_takeaway_artifact(self, artifact_path: str | None) -> dict[str, Any] | None:
    if not artifact_path:
      return None
    artifact_file = get_settings().data_dir.parents[1] / Path(*artifact_path.split("/"))
    if not artifact_file.exists():
      return None
    try:
      artifact = json.loads(artifact_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
      return None
    if artifact.get("artifact_type") != "miroworld_editorial_takeaway":
      return None
    takeaway = artifact.get("takeaway")
    return takeaway if isinstance(takeaway, dict) else None

  def _build_context(self, snapshot: ProjectSnapshot, language: DisplayLanguage) -> dict[str, Any]:
    world_state = snapshot.world_state
    progress = world_state.theatre_progress
    events = world_state.key_events
    revealed_count = max(1, min(progress.revealed_event_count, len(events) or 1))
    revealed_events = events[:revealed_count]
    selected_event = next(
      (event for event in events if event.event_id == progress.selected_event_id),
      revealed_events[-1] if revealed_events else events[0],
    )
    selected_branch = next(
      (branch for branch in selected_event.branches if branch.branch_id == progress.selected_branch_id),
      selected_event.branches[0],
    )
    selected_cost = next(
      (lens for lens in world_state.cost_lenses if lens.target_branch_id == selected_branch.branch_id),
      None,
    )
    latest_calibrations = world_state.calibration_records[:6]

    return {
      "project_id": snapshot.project.project_id,
      "language": language,
      "headline": world_state.headline,
      "summary": world_state.summary,
      "revealed_event_count": revealed_count,
      "total_event_count": len(events),
      "selected_event": {
        "event_id": selected_event.event_id,
        "title": selected_event.title,
        "summary": selected_event.summary,
        "impact_level": selected_event.impact_level,
        "affected_entities": selected_event.affected_entities[:6],
      },
      "selected_branch": {
        "branch_id": selected_branch.branch_id,
        "label": selected_branch.label,
        "description": selected_branch.description,
        "confidence": selected_branch.effective_confidence or selected_branch.confidence,
        "cost_hint": selected_branch.cost_hint,
        "premises": selected_branch.premises[:4],
        "signals_for": selected_branch.signals_for[:3],
        "signals_against": selected_branch.signals_against[:3],
      },
      "revealed_track": [
        {
          "event_id": event.event_id,
          "title": event.title,
          "stage": event.stage,
          "primary_branch": event.branches[0].label if event.branches else "",
        }
        for event in revealed_events
      ],
      "cost": {
        "first_order": selected_cost.first_order_costs[:3] if selected_cost else [],
        "second_order": selected_cost.second_order_costs[:3] if selected_cost else [],
        "ethical_notes": selected_cost.ethical_notes[:3] if selected_cost else [],
      },
      "ripple": {
        "latest_bend": world_state.replay_trace[0].summary if world_state.replay_trace else "",
        "cards": [
          {
            "event_title": item.event_title,
            "branch_label": item.branch_label,
            "summary": item.summary,
          }
          for item in world_state.replay_trace[:4]
        ],
      },
      "archive": {
        "decision_count": len(world_state.player_decision_log),
        "calibration_count": len(world_state.calibration_records),
        "latest_calibrations": [
          {
            "event_id": record.event_id,
            "branch_id": record.branch_id,
            "result": record.result,
            "actual_outcome": record.actual_outcome,
          }
          for record in latest_calibrations
        ],
      },
    }

  def _fallback_takeaway(self, context: dict[str, Any], language: DisplayLanguage) -> dict[str, Any]:
    branch = context["selected_branch"]
    event = context["selected_event"]
    revealed = f"{context['revealed_event_count']}/{context['total_event_count']}"
    calibration_count = context["archive"]["calibration_count"]
    ripple_summary = context["ripple"]["latest_bend"] or event["summary"]
    if language == "zh":
      return {
        "title": f"{event['title']} / 后台编辑读法",
        "summary": f"这条世界线已经显影到 {revealed} 个节点，当前分支“{branch['label']}”把规则、材料、环境和行动者压到同一个代价场里。",
        "takeaways": [
          f"当前分支不是答案，而是一个仍在受条件牵引的轨道；置信度约为 {round(branch['confidence'] * 100)}%。",
          f"代价线索集中在：{branch['cost_hint'] or '尚未完全显影的压力分配'}。",
          f"Archive 已写入 {calibration_count} 条真实结果；之后的校准会继续改写这条轨道的残影。",
        ],
        "ripple_note": f"回响读法：{ripple_summary}",
        "calibration_note": "校准不是给预测打分，而是把后来发生的事实写回世界线。",
        "intervention_note": "合适的干涉点应当落在高代价或高不确定的节点，而不是在结尾等待结论。",
        "disclaimer": "这是面向观众的世界推演读法，不是确定性预测，也不暴露模型隐藏推理。",
      }
    return {
      "title": f"{event['title']} / backstage editorial reading",
      "summary": f"The worldline has exposed {revealed} node(s). The current branch, \"{branch['label']}\", pulls rules, materials, environments, and actors into one cost field.",
      "takeaways": [
        f"The branch is not an answer; it is a track still being pulled by conditions, with roughly {round(branch['confidence'] * 100)}% confidence.",
        f"The cost cue is: {branch['cost_hint'] or 'a pressure distribution still being exposed'}.",
        f"Archive contains {calibration_count} actual outcome(s); later calibration can keep rewriting the afterimage of this orbit.",
      ],
      "ripple_note": f"Ripple reading: {ripple_summary}",
      "calibration_note": "Calibration is not an accuracy score; it writes later facts back into the worldline.",
      "intervention_note": "The useful intervention point is a high-cost or high-uncertainty node, not the passive wait for an ending.",
      "disclaimer": "This is a public worldline reading, not a deterministic prediction, and it does not expose hidden model reasoning.",
    }

  def _normalize_packet(self, packet: dict[str, Any] | None, fallback: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(packet, dict):
      return None
    raw_takeaways = packet.get("takeaways")
    if not isinstance(raw_takeaways, list):
      return None
    takeaways = [str(item).strip() for item in raw_takeaways if str(item).strip()][:5]
    if len(takeaways) < 2:
      return None
    return {
      "title": self._clean_field(packet.get("title"), fallback["title"]),
      "summary": self._clean_field(packet.get("summary"), fallback["summary"]),
      "takeaways": takeaways,
      "ripple_note": self._clean_field(packet.get("ripple_note"), fallback["ripple_note"]),
      "calibration_note": self._clean_field(packet.get("calibration_note"), fallback["calibration_note"]),
      "intervention_note": self._clean_field(packet.get("intervention_note"), fallback["intervention_note"]),
      "disclaimer": self._clean_field(packet.get("disclaimer"), fallback["disclaimer"]),
    }

  def _write_result(
    self,
    snapshot: ProjectSnapshot,
    language: DisplayLanguage,
    context: dict[str, Any],
    takeaway: dict[str, Any],
    *,
    status: str,
    source: str,
    summary: str,
  ) -> dict[str, Any]:
    generated_at = utc_now()
    project_id = snapshot.project.project_id
    artifact_id = make_id("editorial")
    relative_path = f"data/runtime/process/{project_id}/editorial/{artifact_id}/00-editorial-takeaway.json"
    artifact_file = get_settings().data_dir / "process" / project_id / "editorial" / artifact_id / "00-editorial-takeaway.json"
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    public_takeaway = {
      **takeaway,
      "source": source,
      "generated_at": generated_at,
    }
    artifact = {
      "generated_at": generated_at,
      "artifact_type": "miroworld_editorial_takeaway",
      "operation": "editorial_takeaway",
      "project_id": project_id,
      "language": language,
      "status": status,
      "provider": "MiniMax" if source == "minimax" else "local",
      "model_name": self.llm_adapter.settings.llm_model_name if source == "minimax" else "deterministic-fallback",
      "takeaway": public_takeaway,
      "context_digest": {
        "revealed_event_count": context["revealed_event_count"],
        "total_event_count": context["total_event_count"],
        "selected_event_id": context["selected_event"]["event_id"],
        "selected_branch_id": context["selected_branch"]["branch_id"],
        "calibration_count": context["archive"]["calibration_count"],
      },
      "note": "This artifact stores only public editorial output and compact context metadata; it never stores API keys or raw hidden model reasoning.",
    }
    artifact_file.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
      "status": status,
      "progress_step": "editorial_ready" if status == "completed" else "fallback",
      "summary": summary,
      "artifact_path": relative_path,
    }

  def _fallback_summary(self) -> str:
    error = self.llm_adapter.last_error
    if not error:
      return "MiniMax editorial output was unavailable; local editorial fallback is ready."
    return f"MiniMax editorial output was unavailable ({error}); local editorial fallback is ready."

  def _clean_field(self, value: Any, fallback: str) -> str:
    text = str(value).strip() if value is not None else ""
    return text[:900] if text else fallback

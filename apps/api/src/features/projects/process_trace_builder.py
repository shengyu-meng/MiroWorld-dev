from __future__ import annotations

import json
from pathlib import Path

from config import get_settings
from shared.utils import utc_now

from .models import Branch, CostLens, DisplayLanguage, KeyEvent, WorldState


class ProcessTraceBuilder:
  def build(self, world_state: WorldState, language: DisplayLanguage) -> dict:
    generated_at = utc_now()
    run_id = f"proc_{world_state.project_id}_v{world_state.version}"
    relative_root = f"data/runtime/process/{world_state.project_id}/v{world_state.version}"
    absolute_root = get_settings().data_dir / "process" / world_state.project_id / f"v{world_state.version}"
    absolute_root.mkdir(parents=True, exist_ok=True)

    steps = [
      self._build_step(
        world_state=world_state,
        event=event,
        index=index,
        relative_root=relative_root,
        absolute_root=absolute_root,
        generated_at=generated_at,
        language=language,
      )
      for index, event in enumerate(world_state.key_events)
    ]

    return {
      "run_id": run_id,
      "generated_at": generated_at,
      "artifact_root": relative_root,
      "storage_mode": "local_gitignored_runtime",
      "reasoning_run": self._reasoning_run_preview(world_state),
      "steps": steps,
    }

  def _reasoning_run_preview(self, world_state: WorldState) -> dict | None:
    if not world_state.reasoning_runs:
      return None
    latest = world_state.reasoning_runs[0]
    return {
      "reasoning_run_id": latest.reasoning_run_id,
      "provider": latest.provider,
      "model_name": latest.model_name,
      "status": latest.status,
      "artifact_path": latest.artifact_path,
      "summary": latest.summary,
      "step_count": latest.step_count,
    }

  def _build_step(
    self,
    world_state: WorldState,
    event: KeyEvent,
    index: int,
    relative_root: str,
    absolute_root: Path,
    generated_at: str,
    language: DisplayLanguage,
  ) -> dict:
    primary_branch = self._primary_branch(event)
    target_lenses = [lens for lens in world_state.cost_lenses if lens.target_branch_id == primary_branch.branch_id]
    counter_signal_count = len(primary_branch.signals_against)
    cost_mass = self._cost_mass(target_lenses)
    is_open = event.impact_level == "high" or counter_signal_count > 0 or cost_mass >= 4
    recommended_input_type = self._recommended_input_type(event, counter_signal_count)
    effect_scope = self._effect_scope_for(recommended_input_type)
    artifact_name = f"{index + 1:02d}-{event.event_id}-process.json"
    artifact_path = f"{relative_root}/{artifact_name}"

    step = {
      "step_id": f"step_{index + 1:02d}_{event.event_id}",
      "event_id": event.event_id,
      "event_title": event.title,
      "branch_id": primary_branch.branch_id,
      "branch_label": primary_branch.label,
      "status": "ready",
      "artifact_path": artifact_path,
      "artifact_kind": "runtime_json",
      "summary": self._t(
        language,
        f"后台已把 {event.title} 拆成事实、推断、价值和行动四层，可在此决定是否介入。",
        f"The backend has split {event.title} into fact, inference, value, and action layers.",
      ),
      "layer_results": [
        self._fact_layer(event, language),
        self._inference_layer(primary_branch, counter_signal_count, language),
        self._value_layer(target_lenses, cost_mass, language),
        self._action_layer(recommended_input_type, effect_scope, is_open, language),
      ],
      "intervention_window": {
        "is_open": is_open,
        "urgency": self._urgency(event, counter_signal_count, cost_mass),
        "recommended_input_type": recommended_input_type,
        "effect_scope": effect_scope,
        "target_event_id": event.event_id,
        "target_branch_id": primary_branch.branch_id,
        "prompt": self._intervention_prompt(event, recommended_input_type, language),
        "reason": self._intervention_reason(event, counter_signal_count, cost_mass, language),
      },
      "artifact_preview": {
        "event_id": event.event_id,
        "primary_confidence": primary_branch.effective_confidence or primary_branch.confidence,
        "counter_signal_count": counter_signal_count,
        "cost_mass": cost_mass,
      },
    }

    self._write_artifact(absolute_root / artifact_name, step, generated_at)
    return step

  def _write_artifact(self, path: Path, step: dict, generated_at: str) -> None:
    payload = {
      "generated_at": generated_at,
      "artifact_type": "miroworld_process_trace_step",
      "step": step,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

  def _primary_branch(self, event: KeyEvent) -> Branch:
    return next((branch for branch in event.branches if branch.visibility == "primary"), event.branches[0])

  def _cost_mass(self, lenses: list[CostLens]) -> int:
    return sum(
      len(lens.first_order_costs)
      + len(lens.second_order_costs)
      + len(lens.affected_groups)
      + len(lens.ethical_notes)
      for lens in lenses
    )

  def _recommended_input_type(self, event: KeyEvent, counter_signal_count: int) -> str:
    if event.impact_level == "high":
      return "intervention"
    if counter_signal_count > 1:
      return "correction"
    if event.impact_level == "medium":
      return "preference"
    return "observation"

  def _effect_scope_for(self, input_type: str) -> str:
    if input_type == "observation":
      return "evidence"
    if input_type == "preference":
      return "ranking"
    return "world_state"

  def _urgency(self, event: KeyEvent, counter_signal_count: int, cost_mass: int) -> str:
    if event.impact_level == "high" or cost_mass >= 6:
      return "high"
    if event.impact_level == "medium" or counter_signal_count > 0:
      return "medium"
    return "low"

  def _fact_layer(self, event: KeyEvent, language: DisplayLanguage) -> dict:
    return {
      "layer": "FACT",
      "title": self._t(language, "事实层扫描", "Fact scan"),
      "inputs": self._limit(event.evidence_notes + event.affected_entities),
      "outputs": [
        self._t(language, f"{len(event.evidence_notes)} 条可观测痕迹", f"{len(event.evidence_notes)} observable traces"),
        self._t(language, f"{len(event.affected_entities)} 个作用体进入场域", f"{len(event.affected_entities)} actants enter the field"),
      ],
      "confidence_note": self._t(language, "只记录可见材料，不把解释伪装成事实。", "Only visible material is recorded here."),
    }

  def _inference_layer(self, branch: Branch, counter_signal_count: int, language: DisplayLanguage) -> dict:
    confidence = branch.effective_confidence or branch.confidence
    return {
      "layer": "INFERENCE",
      "title": self._t(language, "推断层折叠", "Inference fold"),
      "inputs": self._limit(branch.premises + branch.signals_for),
      "outputs": [
        self._t(language, f"主轨置信度 {round(confidence * 100)}%", f"Primary confidence {round(confidence * 100)}%"),
        self._t(language, f"{counter_signal_count} 条反向牵引信号", f"{counter_signal_count} counter-pull signals"),
      ],
      "confidence_note": self._t(language, "置信度绑定到分支，不生成全局准确率。", "Confidence stays attached to the branch."),
    }

  def _value_layer(self, lenses: list[CostLens], cost_mass: int, language: DisplayLanguage) -> dict:
    affected_groups = self._limit([group for lens in lenses for group in lens.affected_groups])
    ethical_notes = self._limit([note for lens in lenses for note in lens.ethical_notes])
    return {
      "layer": "VALUE",
      "title": self._t(language, "代价质量估计", "Cost-mass estimate"),
      "inputs": affected_groups + ethical_notes,
      "outputs": [
        self._t(language, f"代价质量 {cost_mass}", f"Cost mass {cost_mass}"),
        self._t(language, f"{len(affected_groups)} 个承压对象", f"{len(affected_groups)} pressure carriers"),
      ],
      "confidence_note": self._t(language, "这里显示选择的代价，而不是替观众做道德结论。", "This exposes cost without making the moral choice for the viewer."),
    }

  def _action_layer(self, input_type: str, effect_scope: str, is_open: bool, language: DisplayLanguage) -> dict:
    return {
      "layer": "ACTION",
      "title": self._t(language, "行动窗口", "Action window"),
      "inputs": [
        self._t(language, f"建议扰动类型：{input_type}", f"Suggested disturbance: {input_type}"),
        self._t(language, f"作用范围：{effect_scope}", f"Effect scope: {effect_scope}"),
      ],
      "outputs": [
        self._t(language, "窗口已打开" if is_open else "继续观测更合适", "Window open" if is_open else "Keep observing"),
      ],
      "confidence_note": self._t(language, "介入会改变后续轨道；观测可以只增加材料。", "Intervention changes later tracks; observation can simply add material."),
    }

  def _intervention_prompt(self, event: KeyEvent, input_type: str, language: DisplayLanguage) -> str:
    labels = {
      "observation": ("观测", "observation"),
      "correction": ("修正", "correction"),
      "intervention": ("介入", "intervention"),
      "preference": ("偏好约束", "preference constraint"),
    }
    zh_label, en_label = labels.get(input_type, labels["intervention"])
    return self._t(
      language,
      f"在“{event.title}”写入一次{zh_label}：你想让哪条材料、规则或作用体改变轨道？",
      f"Add one {en_label} at \"{event.title}\": which material, rule, or actant should bend the track?",
    )

  def _intervention_reason(self, event: KeyEvent, counter_signal_count: int, cost_mass: int, language: DisplayLanguage) -> str:
    return self._t(
      language,
      f"节点影响级别为 {event.impact_level}，反向信号 {counter_signal_count} 条，代价质量 {cost_mass}。",
      f"Impact is {event.impact_level}; counter-signals {counter_signal_count}; cost mass {cost_mass}.",
    )

  def _limit(self, values: list[str], limit: int = 4) -> list[str]:
    return [value for value in values if value][:limit]

  def _t(self, language: DisplayLanguage, zh: str, en: str) -> str:
    return zh if language == "zh" else en

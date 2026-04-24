from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, replace
from typing import Any

from config import get_settings
from shared.utils import make_id, utc_now
from .llm_adapter import OpenAICompatibleLLMAdapter
from .models import (
  Branch,
  ConfidenceUpdate,
  CostLens,
  DisplayLanguage,
  KeyEvent,
  KnowledgeItem,
  ProjectRecord,
  ProjectSnapshot,
  ReasoningRunRecord,
  ReplayTraceItem,
  ShareArtifact,
  SourceEntity,
  WorldState,
)


@dataclass
class CompiledSeed:
  project: ProjectRecord
  world_state: WorldState


@dataclass
class PromptContext:
  title: str
  summary: str
  seed_words: list[str]
  actants: list[str]
  seed_excerpt: str
  llm_payload: dict[str, Any] | None = None
  llm_events: list[dict[str, Any]] = field(default_factory=list)
  reasoning_steps: list[dict[str, Any]] = field(default_factory=list)
  llm_error: str | None = None

  @property
  def has_llm_reasoning(self) -> bool:
    return self.llm_payload is not None


class SeedCompiler:
  def __init__(self) -> None:
    self.llm_adapter = OpenAICompatibleLLMAdapter()

  def compile_fixture(self, fixture: dict, language: DisplayLanguage) -> ProjectSnapshot:
    project_id = make_id("proj")
    world_state_id = make_id("ws")
    session_id = make_id("sess")
    now = utc_now()
    title = fixture["title"]
    summary = self._translate(
      language,
      f"{fixture['summary']} 观察者会在这条世界线里观察规则、材料、环境与行动者如何共同改写代价和后果。",
      f"{fixture['summary']} The observer watches rules, materials, environments, and actors redistribute cost and consequence.",
    )
    project = ProjectRecord(
      project_id=project_id,
      title=title,
      source_mode="fixture",
      source_label=fixture["fixture_id"],
      created_at=now,
      updated_at=now,
      language=language,
    )
    world_state = self._build_world_state(
      world_state_id=world_state_id,
      project=project,
      session_id=session_id,
      title=title,
      summary=summary,
      seed_words=fixture.get("expected_world_feel") or [],
      source_label=fixture["fixture_id"],
      language=language,
    )
    return ProjectSnapshot(project=project, world_state=world_state)

  def compile_prompt(self, seed_prompt: str, language: DisplayLanguage) -> ProjectSnapshot:
    project_id = make_id("proj")
    world_state_id = make_id("ws")
    session_id = make_id("sess")
    now = utc_now()
    context = self._build_prompt_context(seed_prompt, language)
    context = self._maybe_enrich_prompt_context(context, seed_prompt, language)
    project = ProjectRecord(
      project_id=project_id,
      title=context.title,
      source_mode="seed_prompt",
      source_label="seed_prompt",
      seed_prompt=seed_prompt,
      created_at=now,
      updated_at=now,
      language=language,
    )
    source_label = "seed_prompt+MiniMax" if context.has_llm_reasoning else "seed_prompt"
    world_state = self._build_prompt_world_state(
      world_state_id=world_state_id,
      project=project,
      session_id=session_id,
      context=context,
      source_label=source_label,
      language=language,
    )
    return ProjectSnapshot(project=project, world_state=world_state)

  def _build_prompt_context(self, seed_prompt: str, language: DisplayLanguage) -> PromptContext:
    normalized = " ".join(seed_prompt.strip().split())
    if not normalized:
      normalized = self._translate(
        language,
        "一条未命名的世界线正在形成，规则、物体、环境和行动者尚未稳定。",
        "An unnamed worldline is forming before its rules, objects, environments, and actors stabilize.",
      )
    seed_words = self._extract_seed_words(normalized, language)
    title = self._prompt_title(normalized, seed_words, language)
    summary = self._translate(
      language,
      f"{normalized} 这条 seed 会先形成可推进世界线；如果本地 MiniMax 可用，后台会写入结构化推理包。",
      f"{normalized} This seed first forms an advanceable worldline; when local MiniMax is available, a structured reasoning packet is written into the runtime.",
    )
    return PromptContext(
      title=title,
      summary=summary,
      seed_words=seed_words,
      actants=self._derive_actants(seed_words, language),
      seed_excerpt=self._excerpt(normalized, 120),
    )

  def _maybe_enrich_prompt_context(self, context: PromptContext, seed_prompt: str, language: DisplayLanguage) -> PromptContext:
    if not self.llm_adapter.settings.llm_seed_compiler_enabled:
      return context

    llm_payload = self.llm_adapter.generate_json(
      operation="seed_compiler",
      language=language,
      payload={
        "task": (
          "Build a structured worldline reasoning packet for an art-first simulation theatre. "
          "The world can include humans, institutions, rules, environments, natural objects, materials, energy, and time constraints. "
          "Avoid media-dashboard framing. Do not expose hidden chain-of-thought; return concise public reasoning steps only."
        ),
        "language": language,
        "seed_prompt": seed_prompt,
        "required_json_schema": {
          "title": "short exhibit title",
          "summary": "one paragraph world-simulation premise",
          "seed_words": ["3 to 6 concrete forces, materials, rules, or actants"],
          "actants": ["4 to 6 affected actants, including non-human or rule objects"],
          "reasoning_steps": [
            {
              "layer": "FACT|INFERENCE|VALUE|ACTION",
              "title": "short public-facing step label",
              "inputs": ["visible inputs used by this step"],
              "outputs": ["public-facing result of this step"],
              "confidence_note": "why this layer is provisional",
              "confidence": 0.0,
            }
          ],
          "events": [
            {
              "stage": "Entry/Bend/Ripple or localized equivalent",
              "title": "worldline node title",
              "summary": "what changes at this node",
              "impact_level": "high|medium|low",
              "affected_entities": ["actants affected"],
              "evidence_notes": ["visible evidence or trace"],
              "causal_note": "how this node follows from the previous one",
              "branches": [
                {
                  "label": "branch label",
                  "description": "branch meaning",
                  "confidence": 0.0,
                  "premises": ["conditions that make it hold"],
                  "signals_for": ["signals supporting it"],
                  "signals_against": ["signals resisting it"],
                  "cost_hint": "cost of this branch",
                }
              ],
            }
          ],
        },
      },
    )
    if not llm_payload:
      if self.llm_adapter.settings.llm_api_key:
        return replace(
          context,
          llm_error=self._safe_text(self.llm_adapter.last_error) or "MiniMax did not return structured JSON.",
        )
      return context

    title = self._safe_text(llm_payload.get("title")) or context.title
    summary = self._safe_text(llm_payload.get("summary")) or context.summary
    seed_words = self._safe_list(llm_payload.get("seed_words")) or context.seed_words
    actants = self._safe_list(llm_payload.get("actants")) or context.actants
    return PromptContext(
      title=self._excerpt(title, 72),
      summary=summary,
      seed_words=self._pad_terms(seed_words, self._fallback_seed_words(language)),
      actants=self._pad_terms(actants, self._fallback_actants(language)),
      seed_excerpt=context.seed_excerpt,
      llm_payload=self._sanitize_llm_payload(llm_payload),
      llm_events=self._safe_event_specs(llm_payload.get("events")),
      reasoning_steps=self._safe_reasoning_steps(llm_payload.get("reasoning_steps")),
    )

  def _build_prompt_world_state(
    self,
    *,
    world_state_id: str,
    project: ProjectRecord,
    session_id: str,
    context: PromptContext,
    source_label: str,
    language: DisplayLanguage,
  ) -> WorldState:
    entities = self._build_prompt_entities(context, language)
    knowledge_items = self._build_prompt_knowledge(context, language)
    key_events = self._build_prompt_events(world_state_id, language, context)
    primary_branch = key_events[0].branches[0]
    share_artifact = self._build_share_artifact(context.title, context.summary, language)
    reasoning_runs = self._build_reasoning_runs(project.project_id, context, language)

    return WorldState(
      world_state_id=world_state_id,
      project_id=project.project_id,
      session_id=session_id,
      version=1,
      status="active",
      headline=context.title,
      summary=context.summary,
      source_mode="project_graph",
      source_label=source_label,
      disclaimer=share_artifact.disclaimer,
      share_context=self._translate(
        language,
        "MiniMax 世界线推理" if context.has_llm_reasoning else "Prompt 世界线即时编译",
        "MiniMax worldline reasoning" if context.has_llm_reasoning else "Prompt worldline instant compilation",
      ),
      share_artifact=share_artifact,
      entities=entities,
      key_events=key_events,
      cost_lenses=self._build_cost_lenses(key_events, language, context.actants),
      knowledge_items=knowledge_items,
      confidence_updates=[
        ConfidenceUpdate(
          update_id=make_id("cu"),
          target_type="branch",
          target_id=primary_branch.branch_id,
          before=0.5,
          after=primary_branch.confidence,
          reason=self._translate(
            language,
            "MiniMax 结构化推理包形成了第一条可推进主轨。" if context.has_llm_reasoning else "Prompt 中的作用体、规则和环境信号已经足够形成第一条可推进主轨。",
            "The MiniMax structured reasoning packet formed the first advanceable main track." if context.has_llm_reasoning else "The prompt contains enough actant, rule, and environment signals to form a first advanceable main track.",
          ),
          method="minimax_seed_reasoning" if context.has_llm_reasoning else "deterministic_seed_compile",
          created_at=utc_now(),
        )
      ],
      reasoning_runs=reasoning_runs,
      replay_trace=[
        ReplayTraceItem(
          trace_id=make_id("rt"),
          event_id=key_events[0].event_id,
          event_title=key_events[0].title,
          branch_id=primary_branch.branch_id,
          branch_label=primary_branch.label,
          summary=self._translate(
            language,
            "MiniMax 推理已写入第一层显影轨道，用户可以继续推进或在窗口介入。" if context.has_llm_reasoning else "Prompt 已被写入第一层显影轨道，用户可以直接继续推进或在窗口介入。",
            "MiniMax reasoning has been written into the first exposure track; the viewer can advance or intervene immediately." if context.has_llm_reasoning else "The prompt has been written into the first exposure track; the viewer can advance or intervene immediately.",
          ),
        )
      ],
      created_at=utc_now(),
      updated_at=utc_now(),
    )

  def _build_reasoning_runs(self, project_id: str, context: PromptContext, language: DisplayLanguage) -> list[ReasoningRunRecord]:
    if not context.has_llm_reasoning and not context.llm_error:
      return []
    created_at = utc_now()
    if context.llm_error:
      relative_path = f"data/runtime/process/{project_id}/v1/00-minimax-seed-fallback.json"
      absolute_path = get_settings().data_dir / "process" / project_id / "v1" / "00-minimax-seed-fallback.json"
      absolute_path.parent.mkdir(parents=True, exist_ok=True)
      artifact = {
        "generated_at": created_at,
        "artifact_type": "miroworld_minimax_seed_fallback",
        "provider": "MiniMax",
        "model_name": self.llm_adapter.settings.llm_model_name,
        "language": language,
        "seed_excerpt": context.seed_excerpt,
        "status": "fallback",
        "error": context.llm_error,
        "fallback": "deterministic_seed_compile",
        "note": "No secret or raw provider hidden reasoning is stored in this artifact.",
      }
      absolute_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
      return [
        ReasoningRunRecord(
          reasoning_run_id=make_id("rr"),
          operation="seed_compiler",
          provider="MiniMax",
          model_name=self.llm_adapter.settings.llm_model_name,
          status="fallback",
          artifact_path=relative_path,
          summary=self._translate(
            language,
            "MiniMax reasoning did not complete; fallback reason was recorded and local seed compilation was used.",
            "MiniMax reasoning did not complete; the fallback reason was recorded and local seed compilation was used.",
          ),
          step_count=0,
          created_at=created_at,
        )
      ]

    relative_path = f"data/runtime/process/{project_id}/v1/00-minimax-seed-reasoning.json"
    absolute_path = get_settings().data_dir / "process" / project_id / "v1" / "00-minimax-seed-reasoning.json"
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
      "generated_at": created_at,
      "artifact_type": "miroworld_minimax_seed_reasoning",
      "provider": "MiniMax",
      "model_name": self.llm_adapter.settings.llm_model_name,
      "language": language,
      "seed_excerpt": context.seed_excerpt,
      "title": context.title,
      "summary": context.summary,
      "actants": context.actants,
      "seed_words": context.seed_words,
      "reasoning_steps": context.reasoning_steps,
      "events": context.llm_events,
      "note": "Raw provider hidden reasoning is not stored; this artifact contains the structured public reasoning packet only.",
    }
    absolute_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    return [
      ReasoningRunRecord(
        reasoning_run_id=make_id("rr"),
        operation="seed_compiler",
        provider="MiniMax",
        model_name=self.llm_adapter.settings.llm_model_name,
        status="completed",
        artifact_path=relative_path,
        summary=self._translate(
          language,
          f"MiniMax 生成了 {len(context.llm_events)} 个推演节点和 {len(context.reasoning_steps)} 个公开推理层。",
          f"MiniMax generated {len(context.llm_events)} worldline nodes and {len(context.reasoning_steps)} public reasoning layers.",
        ),
        step_count=len(context.reasoning_steps) or len(context.llm_events),
        created_at=created_at,
      )
    ]

  def _build_prompt_entities(self, context: PromptContext, language: DisplayLanguage) -> list[SourceEntity]:
    kinds = ["agent", "system", "environment", "constraint", "agent", "environment"]
    descriptions = [
      self._translate(language, "最先改变轨道方向的作用体。", "The actant that first redirects the track."),
      self._translate(language, "决定阈值、边界和可行动作的规则层。", "The rule layer that sets thresholds, boundaries, and possible actions."),
      self._translate(language, "让变化获得速度或阻力的场域条件。", "The field condition that gives the change speed or resistance."),
      self._translate(language, "时间、材料、能量或资源形成的约束。", "Constraints formed by time, material, energy, or resources."),
      self._translate(language, "被世界线推挤但仍可能反向改变路径的对象。", "A pressured object that may still bend the path back."),
      self._translate(language, "在后续节点中保留痕迹的环境残影。", "An environmental afterimage that persists into later nodes."),
    ]
    return [
      SourceEntity(
        entity_id=make_id("ent"),
        entity_kind=kinds[index % len(kinds)],
        name=name,
        description=descriptions[index % len(descriptions)],
      )
      for index, name in enumerate(context.actants[:6])
    ]

  def _build_prompt_knowledge(self, context: PromptContext, language: DisplayLanguage) -> list[KnowledgeItem]:
    if context.reasoning_steps:
      items: list[KnowledgeItem] = []
      for step in context.reasoning_steps[:8]:
        layer = self._coerce_layer(step.get("layer"))
        content = self._safe_text(step.get("outputs", [""])[0] if isinstance(step.get("outputs"), list) and step.get("outputs") else step.get("title")) or self._safe_text(step.get("confidence_note"))
        if not content:
          continue
        items.append(
          KnowledgeItem(
            id=make_id("ki"),
            layer=layer,
            content=content,
            source_type="minimax_reasoning",
            confidence=self._clamp_float(step.get("confidence"), 0.74),
          )
        )
      if items:
        return items

    lead, rule, field, constraint = context.actants[:4]
    return [
      KnowledgeItem(id=make_id("ki"), layer="FACT", content=self._translate(language, f"Seed 中明确出现了 {context.seed_excerpt}", f"The seed explicitly contains: {context.seed_excerpt}"), source_type="seed_prompt", confidence=0.86),
      KnowledgeItem(id=make_id("ki"), layer="INFERENCE", content=self._translate(language, f"{lead} 与 {rule} 正在形成第一组因果牵引。", f"{lead} and {rule} are forming the first causal pull."), source_type="deterministic_compile", confidence=0.72),
      KnowledgeItem(id=make_id("ki"), layer="VALUE", content=self._translate(language, f"代价不会平均分布，{field} 与 {constraint} 会先承受压力。", f"Cost will not distribute evenly; {field} and {constraint} will carry early pressure."), source_type="deterministic_compile", confidence=0.7),
      KnowledgeItem(id=make_id("ki"), layer="ACTION", content=self._translate(language, "每个节点都会开放一个合适的干涉窗口：观测、修正、介入或偏好约束。", "Each node opens a suitable intervention window: observation, correction, intervention, or preference constraint."), source_type="system", confidence=0.78),
    ]

  def _build_world_state(
    self,
    *,
    world_state_id: str,
    project: ProjectRecord,
    session_id: str,
    title: str,
    summary: str,
    seed_words: list[str],
    source_label: str,
    language: DisplayLanguage,
  ) -> WorldState:
    context = PromptContext(
      title=title,
      summary=summary,
      seed_words=self._pad_terms(seed_words, self._fallback_seed_words(language)),
      actants=self._fallback_actants(language),
      seed_excerpt=self._translate(language, "预设世界线", "fixture worldline"),
    )
    entities = self._build_prompt_entities(context, language)
    key_events = self._build_events(world_state_id, language, seed_words)
    primary_branch = key_events[0].branches[0]
    share_artifact = self._build_share_artifact(title, summary, language)

    return WorldState(
      world_state_id=world_state_id,
      project_id=project.project_id,
      session_id=session_id,
      version=1,
      status="active",
      headline=title,
      summary=summary,
      source_mode="fixture" if project.source_mode == "fixture" else "project_graph",
      source_label=source_label,
      disclaimer=share_artifact.disclaimer,
      share_context=self._translate(language, "世界推演体验 MVP", "World-simulation experience MVP"),
      share_artifact=share_artifact,
      entities=entities,
      key_events=key_events,
      cost_lenses=self._build_cost_lenses(key_events, language),
      knowledge_items=[
        KnowledgeItem(id=make_id("ki"), layer="FACT", content=self._translate(language, "触发材料已经进入可观测层。", "The triggering material has entered the observable layer."), source_type="fixture", confidence=0.82),
        KnowledgeItem(id=make_id("ki"), layer="INFERENCE", content=self._translate(language, "最初的解释框架会决定后续世界线的分叉角度。", "The first interpretation frame will determine how the worldline forks."), source_type="system", confidence=0.68),
        KnowledgeItem(id=make_id("ki"), layer="VALUE", content=self._translate(language, "系统会暴露谁承担代价，以及什么被视为可接受的损耗。", "The system exposes who absorbs the cost and what counts as acceptable loss."), source_type="system", confidence=0.73),
        KnowledgeItem(id=make_id("ki"), layer="ACTION", content=self._translate(language, "一次清晰但有代价的 intervention 会显著改变后续轨迹。", "A clear but costly intervention can noticeably bend the next trajectory."), source_type="system", confidence=0.76),
      ],
      confidence_updates=[
        ConfidenceUpdate(update_id=make_id("cu"), target_type="branch", target_id=primary_branch.branch_id, before=0.55, after=primary_branch.confidence, reason=self._translate(language, "多条早期信号在主分支上汇聚。", "Multiple early signals converge on the main branch."), method="rule", created_at=utc_now())
      ],
      replay_trace=[
        ReplayTraceItem(trace_id=make_id("rt"), event_id=key_events[0].event_id, event_title=key_events[0].title, branch_id=primary_branch.branch_id, branch_label=primary_branch.label, summary=self._translate(language, "主分支获得第一轮可见度优势。", "The primary branch gains the first visibility advantage."))
      ],
      created_at=utc_now(),
      updated_at=utc_now(),
    )

  def _build_share_artifact(self, title: str, summary: str, language: DisplayLanguage) -> ShareArtifact:
    return ShareArtifact(
      title=title,
      subtitle=self._translate(language, "不是唯一未来，而是一张判断地图", "Not the only future, but a map of judgment"),
      summary=summary,
      disclaimer=self._translate(language, "这是一件可重演、可校准的判断作品，不是确定性预测。", "This is a replayable, calibratable judgment work, not a deterministic prediction."),
      share_text=self._translate(language, f"我进入了《{title}》的世界线，看见规则、材料、环境和行动如何重新分配代价。", f"I stepped into the worldline of {title} and watched rules, materials, environments, and actions redistribute cost."),
      tags=["miroworld", "worldline", "field-simulation"],
      short_excerpt=self._translate(language, "世界线不是答案，它让代价发光。", "A worldline is not an answer. It makes the cost visible."),
      poster_caption=self._translate(language, "观察分支，承担选择。", "Observe the branch. Carry the choice."),
      curator_note=self._translate(language, "观察者不是旁观者，而是变量。", "The observer is not outside the field, but a variable within it."),
      wall_label=self._translate(language, "一条由判断、误差、规则与代价构成的世界线。", "A worldline made of judgment, error, rules, and cost."),
      archive_summary=self._translate(language, "第一版档案已经建立，后续 replay 与 calibration 会持续写入。", "The first archive is ready; later replays and calibrations will continue to write into it."),
    )

  def _build_prompt_events(self, world_state_id: str, language: DisplayLanguage, context: PromptContext) -> list[KeyEvent]:
    specs = context.llm_events if context.llm_events else self._fallback_event_specs(language, context)
    if len(specs) < 3:
      specs = specs + self._fallback_event_specs(language, context)[len(specs):]
    events: list[KeyEvent] = []
    previous_event_id = ""
    for index, spec in enumerate(specs[:5]):
      event = self._event_from_spec(world_state_id, language, index, previous_event_id, spec)
      events.append(event)
      previous_event_id = event.event_id
    return events

  def _event_from_spec(self, world_state_id: str, language: DisplayLanguage, index: int, previous_event_id: str, spec: dict[str, Any]) -> KeyEvent:
    event_id = make_id("evt")
    branches = self._branches_from_spec(event_id, language, index, spec)
    stage_fallback = ["入口", "折转", "回响", "归档", "再显影"] if language == "zh" else ["Entry", "Bend", "Ripple", "Archive", "Re-entry"]
    return KeyEvent(
      event_id=event_id,
      world_state_id=world_state_id,
      title=self._safe_text(spec.get("title")) or self._translate(language, f"推演节点 {index + 1}", f"Worldline node {index + 1}"),
      summary=self._safe_text(spec.get("summary")) or self._translate(language, "该节点由模型推理包和本地兜底结构共同生成。", "This node is formed from the model packet and local fallback structure."),
      depends_on_event_id=previous_event_id,
      causal_note=self._safe_text(spec.get("causal_note")) or self._translate(language, "上一层形成的约束继续向后传导。", "The previous layer's constraint continues downstream."),
      causal_strength="high" if index == 0 else "medium",
      collapse_hint=self._translate(language, "如果不推进，系统会停留在当前显影层。", "If not advanced, the system remains in the current exposure layer."),
      stage=self._safe_text(spec.get("stage")) or stage_fallback[min(index, len(stage_fallback) - 1)],
      impact_level=self._coerce_impact(spec.get("impact_level"), "high" if index == 0 else "medium"),
      fold_state="expanded" if index == 0 else "collapsed",
      branches=branches,
      evidence_ids=[make_id("ev"), make_id("ev")],
      evidence_notes=self._safe_list(spec.get("evidence_notes"))[:4] or [self._translate(language, "模型推理包给出了该节点的可观测痕迹。", "The model reasoning packet supplied an observable trace for this node.")],
      affected_entities=self._pad_terms(self._safe_list(spec.get("affected_entities")), self._fallback_actants(language), 3)[:5],
    )

  def _branches_from_spec(self, event_id: str, language: DisplayLanguage, index: int, spec: dict[str, Any]) -> list[Branch]:
    branch_specs = spec.get("branches")
    if not isinstance(branch_specs, list) or not branch_specs:
      branch_specs = self._fallback_branch_specs(language)
    branches: list[Branch] = []
    confidences = [(0.64, 0.25, 0.11), (0.56, 0.29, 0.15), (0.51, 0.33, 0.16)][min(index, 2)]
    for branch_index, branch_spec in enumerate(branch_specs[:3]):
      if not isinstance(branch_spec, dict):
        continue
      branches.append(
        Branch(
          branch_id=make_id("br"),
          event_id=event_id,
          label=self._safe_text(branch_spec.get("label")) or self._fallback_branch_specs(language)[branch_index]["label"],
          description=self._safe_text(branch_spec.get("description")) or self._fallback_branch_specs(language)[branch_index]["description"],
          confidence=self._clamp_float(branch_spec.get("confidence"), confidences[min(branch_index, len(confidences) - 1)]),
          premises=self._safe_list(branch_spec.get("premises"))[:4] or [self._translate(language, "可观测材料足以支撑这一轨道继续显影。", "Observable material is sufficient for this track to keep appearing.")],
          signals_for=self._safe_list(branch_spec.get("signals_for"))[:4] or [self._translate(language, "因果链条开始对齐。", "The causal chain begins to align.")],
          signals_against=self._safe_list(branch_spec.get("signals_against"))[:3] or [self._translate(language, "新的观测仍可能改变证据层。", "A new observation may still change the evidence layer.")],
          visibility="primary" if branch_index == 0 else "alternate",
          state="selected" if index == 0 and branch_index == 0 else "candidate",
          cost_hint=self._safe_text(branch_spec.get("cost_hint")) or self._translate(language, "清晰度上升，但代价会更快显形。", "Clarity rises, but cost becomes visible faster."),
        )
      )
    return branches or self._branches_from_spec(event_id, language, index, {"branches": self._fallback_branch_specs(language)})

  def _build_events(self, world_state_id: str, language: DisplayLanguage, seed_words: list[str]) -> list[KeyEvent]:
    context = PromptContext(
      title="",
      summary="",
      seed_words=self._pad_terms(seed_words, self._fallback_seed_words(language)),
      actants=self._fallback_actants(language),
      seed_excerpt=self._translate(language, "预设世界线", "fixture worldline"),
    )
    return self._build_prompt_events(world_state_id, language, context)

  def _build_cost_lenses(self, events: list[KeyEvent], language: DisplayLanguage, actants: list[str] | None = None) -> list[CostLens]:
    targets = self._pad_terms(actants or [], self._fallback_actants(language))
    lenses: list[CostLens] = []
    for event in events:
      for branch in event.branches:
        lenses.append(
          CostLens(
            cost_lens_id=make_id("cl"),
            target_branch_id=branch.branch_id,
            first_order_costs=[
              self._translate(language, f"{targets[0]}的响应窗口被压缩。", f"The response window for {targets[0]} is compressed."),
              self._translate(language, f"{targets[1]}需要承担更早到来的调整压力。", f"{targets[1]} takes earlier adjustment pressure."),
            ],
            second_order_costs=[
              self._translate(language, f"{targets[2]}会保留更长的残影。", f"{targets[2]} retains a longer afterimage."),
              self._translate(language, "后续信任修复会变得更慢、更贵。", "Later trust repair becomes slower and more expensive."),
            ],
            affected_groups=[targets[0], targets[1], targets[2]],
            ethical_notes=[
              self._translate(language, "不要把最顺滑的轨道误认为代价最小的轨道。", "Do not mistake the smoothest track for the lowest-cost track."),
              self._translate(language, "低概率分支也可能包含最大的道德负担。", "Low-probability branches may still contain the largest ethical burden."),
            ],
          )
        )
    return lenses

  def _fallback_event_specs(self, language: DisplayLanguage, context: PromptContext) -> list[dict[str, Any]]:
    lead, rule, field, constraint = context.actants[:4]
    tertiary = context.actants[4] if len(context.actants) > 4 else field
    return [
      {
        "stage": self._translate(language, "入口", "Entry"),
        "impact_level": "high",
        "title": self._translate(language, f"{lead}进入可观测层", f"{lead} enters the observable layer"),
        "summary": self._translate(language, f"{context.seed_excerpt} 开始显影：{lead}、{rule} 与 {field} 被放进同一个作用场。", f"{context.seed_excerpt} begins to appear: {lead}, {rule}, and {field} enter the same field."),
        "affected_entities": [lead, rule, field],
        "evidence_notes": [self._translate(language, f"Seed 线索把 {lead} 与 {rule} 同时推入场域。", f"The seed pushes {lead} and {rule} into the field together.")],
        "causal_note": self._translate(language, "入口事件决定观众最先看见哪一层因果。", "The entry event decides which causal layer appears first."),
        "branches": self._fallback_branch_specs(language),
      },
      {
        "stage": self._translate(language, "折转", "Bend"),
        "impact_level": "medium",
        "title": self._translate(language, f"{constraint}重新分配轨道", f"{constraint} redistributes the track"),
        "summary": self._translate(language, f"{rule}、{constraint} 与 {tertiary} 开始争夺节奏。", f"{rule}, {constraint}, and {tertiary} begin negotiating tempo."),
        "affected_entities": [rule, constraint, tertiary],
        "evidence_notes": [self._translate(language, f"{constraint}的压力正在转移到 {tertiary}。", f"Pressure from {constraint} is moving toward {tertiary}.")],
        "causal_note": self._translate(language, "第一层显影形成的惯性开始改变资源与行动的顺序。", "The inertia from the first exposure changes the ordering of resources and actions."),
        "branches": self._fallback_branch_specs(language),
      },
      {
        "stage": self._translate(language, "回响", "Ripple"),
        "impact_level": "medium",
        "title": self._translate(language, f"{field}沉积为新的世界残影", f"{field} settles into a new world afterimage"),
        "summary": self._translate(language, f"最后一层留下 {lead}、{rule}、{constraint} 之间的代价记录。", f"The last layer leaves a cost record among {lead}, {rule}, and {constraint}."),
        "affected_entities": [field, lead, constraint],
        "evidence_notes": [self._translate(language, f"{field}保留了前两层的弯折痕迹。", f"{field} retains the bends from the first two layers.")],
        "causal_note": self._translate(language, "前两层选择沉积成新的边界条件。", "The first two layers settle into new boundary conditions."),
        "branches": self._fallback_branch_specs(language),
      },
    ]

  def _fallback_branch_specs(self, language: DisplayLanguage) -> list[dict[str, Any]]:
    return [
      {
        "label": self._translate(language, "主轨显影", "Primary exposure"),
        "description": self._translate(language, "世界线沿着最强因果牵引继续推进。", "The worldline advances along the strongest causal pull."),
        "confidence": 0.62,
        "premises": [self._translate(language, "可观测材料已经足以支撑这一轨道。", "Observable material is sufficient to support this track.")],
        "signals_for": [self._translate(language, "代价载体已经可见。", "The cost carrier is visible.")],
        "signals_against": [self._translate(language, "新的观测或修正仍可能改变证据层。", "A new observation or correction may still change the evidence layer.")],
        "cost_hint": self._translate(language, "清晰度上升，但会把代价更快推给承压对象。", "Clarity rises, but cost moves faster onto pressured actants."),
      },
      {
        "label": self._translate(language, "慢速校准", "Slow calibration"),
        "description": self._translate(language, "系统先吸收不确定性，再决定是否折转。", "The system absorbs uncertainty before deciding whether to bend."),
        "confidence": 0.27,
        "premises": [self._translate(language, "观测场仍保留判断弹性。", "The observer field still retains judgment elasticity.")],
        "signals_for": [self._translate(language, "新的细节削弱单一轨道。", "New details weaken the single track.")],
        "signals_against": [self._translate(language, "节奏过慢会扩大不确定期。", "A slow tempo widens uncertainty.")],
        "cost_hint": self._translate(language, "降低误伤，但会拉长不确定窗口。", "Reduces collateral damage but lengthens uncertainty."),
      },
      {
        "label": self._translate(language, "高冲击低概率", "High-impact low-probability"),
        "description": self._translate(language, "脆弱节点被过度放大，可能触发突然折叠。", "A fragile node is over-amplified and may trigger a sudden fold."),
        "confidence": 0.11,
        "premises": [self._translate(language, "脆弱节点被过度放大。", "A fragile node is over-amplified.")],
        "signals_for": [self._translate(language, "风险叙事开始压过事实层。", "Risk framing begins to dominate the fact layer.")],
        "signals_against": [self._translate(language, "稳定结构仍可吸收部分冲击。", "Stable structures can still absorb part of the shock.")],
        "cost_hint": self._translate(language, "可见度极高，但可能制造难以回收的后续损耗。", "Highly visible, but may create downstream damage that is hard to unwind."),
      },
    ]

  def _safe_event_specs(self, value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
      return []
    return [item for item in value if isinstance(item, dict)]

  def _safe_reasoning_steps(self, value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
      return []
    return [item for item in value if isinstance(item, dict)]

  def _sanitize_llm_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
    return {
      "title": self._safe_text(payload.get("title")),
      "summary": self._safe_text(payload.get("summary")),
      "seed_words": self._safe_list(payload.get("seed_words")),
      "actants": self._safe_list(payload.get("actants")),
      "reasoning_steps": self._safe_reasoning_steps(payload.get("reasoning_steps")),
      "events": self._safe_event_specs(payload.get("events")),
    }

  def _extract_seed_words(self, text: str, language: DisplayLanguage) -> list[str]:
    if language == "zh":
      parts = re.split(r"[，。；、！？,.!?;:\s]+", text)
      words = [part.strip("“”\"'()（）") for part in parts if len(part.strip("“”\"'()（）")) >= 2]
    else:
      stopwords = {"the", "and", "with", "from", "into", "that", "this", "when", "where", "their", "worldline"}
      words = [word for word in re.findall(r"[A-Za-z][A-Za-z-]{2,}", text) if word.lower() not in stopwords]
    return self._pad_terms(words[:6], self._fallback_seed_words(language))

  def _derive_actants(self, seed_words: list[str], language: DisplayLanguage) -> list[str]:
    return self._pad_terms(seed_words[:6], self._fallback_actants(language))

  def _fallback_seed_words(self, language: DisplayLanguage) -> list[str]:
    return self._translate(
      language,
      "规则压力|材料约束|环境回声|行动者|时间阈值|能量流向",
      "rule pressure|material constraint|environmental echo|actor|time threshold|energy flow",
    ).split("|")

  def _fallback_actants(self, language: DisplayLanguage) -> list[str]:
    return self._translate(
      language,
      "规则层|材料层|环境条件|时间约束|行动者|世界残影",
      "rule layer|material layer|field condition|time constraint|actor|world afterimage",
    ).split("|")

  def _pad_terms(self, values: list[str], fallback: list[str], target: int = 6) -> list[str]:
    cleaned: list[str] = []
    for value in values + fallback:
      item = self._excerpt(str(value).strip(), 48)
      if item and item not in cleaned:
        cleaned.append(item)
      if len(cleaned) >= target:
        return cleaned
    return cleaned

  def _prompt_title(self, text: str, seed_words: list[str], language: DisplayLanguage) -> str:
    if language == "zh":
      lead = seed_words[0] if seed_words else "世界线"
      return self._excerpt(f"{lead}的折转", 32)
    return self._excerpt(text, 64)

  def _safe_text(self, value: Any) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else ""

  def _safe_list(self, value: Any) -> list[str]:
    if not isinstance(value, list):
      return []
    return [str(item).strip() for item in value if str(item).strip()]

  def _excerpt(self, value: str, limit: int) -> str:
    text = " ".join(value.strip().split())
    if len(text) <= limit:
      return text
    return f"{text[:limit].rstrip()}..."

  def _clamp_float(self, value: Any, fallback: float) -> float:
    try:
      parsed = float(value)
    except (TypeError, ValueError):
      parsed = fallback
    return min(1.0, max(0.0, parsed))

  def _coerce_impact(self, value: Any, fallback: str) -> str:
    return value if value in {"low", "medium", "high"} else fallback

  def _coerce_layer(self, value: Any) -> str:
    return value if value in {"FACT", "INFERENCE", "VALUE", "ACTION"} else "INFERENCE"

  def _translate(self, language: DisplayLanguage, zh: str, en: str) -> str:
    return zh if language == "zh" else en

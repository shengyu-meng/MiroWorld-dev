from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

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
    world_state = self._build_prompt_world_state(
      world_state_id=world_state_id,
      project=project,
      session_id=session_id,
      context=context,
      source_label="seed_prompt",
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
      f"{normalized} 这条 seed 会被立即编译成可观测、可推进、可干涉的世界线，而不是等待实时模型返回。",
      f"{normalized} This seed is compiled immediately into an observable, advanceable, and interruptible worldline instead of waiting on a live model call.",
    )
    actants = self._derive_actants(seed_words, language)
    return PromptContext(
      title=title,
      summary=summary,
      seed_words=seed_words,
      actants=actants,
      seed_excerpt=self._excerpt(normalized, 96),
    )

  def _maybe_enrich_prompt_context(self, context: PromptContext, seed_prompt: str, language: DisplayLanguage) -> PromptContext:
    if not self.llm_adapter.settings.llm_seed_compiler_enabled:
      return context

    llm_payload = self.llm_adapter.generate_json(
      operation="seed_compiler",
      language=language,
      payload={
        "task": "Return a compact worldline seed. Include human and non-human actants. Avoid media-dashboard framing.",
        "schema": {
          "title": "short exhibit title",
          "summary": "one paragraph world-simulation premise",
          "seed_words": ["3 to 6 concrete forces, materials, rules, or actants"],
          "actants": ["4 to 6 affected actants, including non-human or rule objects"],
        },
        "seed_prompt": seed_prompt,
        "language": language,
      },
    )
    if not llm_payload:
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
      share_context=self._translate(language, "Prompt 世界线即时编译", "Prompt worldline instant compilation"),
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
            "Prompt 中的作用体、规则和环境信号已经足够形成第一条可推进主轨。",
            "The prompt contains enough actant, rule, and environment signals to form a first advanceable main track.",
          ),
          method="deterministic_seed_compile",
          created_at=utc_now(),
        )
      ],
      replay_trace=[
        ReplayTraceItem(
          trace_id=make_id("rt"),
          event_id=key_events[0].event_id,
          event_title=key_events[0].title,
          branch_id=primary_branch.branch_id,
          branch_label=primary_branch.label,
          summary=self._translate(
            language,
            "Prompt 已被写入第一层显影轨道，用户可以直接继续推进或在窗口介入。",
            "The prompt has been written into the first exposure track; the viewer can advance or intervene immediately.",
          ),
        )
      ],
      created_at=utc_now(),
      updated_at=utc_now(),
    )

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
    lead = context.actants[0]
    rule = context.actants[1]
    field = context.actants[2]
    constraint = context.actants[3]
    return [
      KnowledgeItem(
        id=make_id("ki"),
        layer="FACT",
        content=self._translate(language, f"Seed 中明确出现了 {context.seed_excerpt}", f"The seed explicitly contains: {context.seed_excerpt}"),
        source_type="seed_prompt",
        confidence=0.86,
      ),
      KnowledgeItem(
        id=make_id("ki"),
        layer="INFERENCE",
        content=self._translate(language, f"{lead} 与 {rule} 正在形成第一组因果牵引。", f"{lead} and {rule} are forming the first causal pull."),
        source_type="deterministic_compile",
        confidence=0.72,
      ),
      KnowledgeItem(
        id=make_id("ki"),
        layer="VALUE",
        content=self._translate(language, f"代价不会平均分布，{field} 与 {constraint} 会先承受压力。", f"Cost will not distribute evenly; {field} and {constraint} will carry early pressure."),
        source_type="deterministic_compile",
        confidence=0.7,
      ),
      KnowledgeItem(
        id=make_id("ki"),
        layer="ACTION",
        content=self._translate(language, "每个节点都会开放一个合适的干涉窗口：观测、修正、介入或偏好约束。", "Each node opens a suitable intervention window: observation, correction, intervention, or preference constraint."),
        source_type="system",
        confidence=0.78,
      ),
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
    entities = [
      SourceEntity(entity_id=make_id("ent"), entity_kind="agent", name=self._translate(language, "触发源", "Trigger source"), description=self._translate(language, "引发这条世界线的人、组织、材料或自然条件。", "The people, groups, materials, or natural conditions that trigger the worldline.")),
      SourceEntity(entity_id=make_id("ent"), entity_kind="system", name=self._translate(language, "规则与制度", "Rules and institutions"), description=self._translate(language, "决定可见度、节奏、阈值与可行动作边界的系统外壳。", "The systems that shape visibility, tempo, thresholds, and possible action.")),
      SourceEntity(entity_id=make_id("ent"), entity_kind="constraint", name=self._translate(language, "资源约束", "Resource pressure"), description=self._translate(language, "成本、时间、材料与注意力限制。", "Limits around cost, time, materials, and attention.")),
      SourceEntity(entity_id=make_id("ent"), entity_kind="environment", name=self._translate(language, "场域条件", "Field conditions"), description=self._translate(language, "环境、时间、自然物与背景压力构成的作用场。", "The field made of environment, timing, natural objects, and background pressure.")),
    ]

    knowledge_items = [
      KnowledgeItem(id=make_id("ki"), layer="FACT", content=self._translate(language, "触发材料已经进入可观测层。", "The triggering material has entered the observable layer."), source_type="fixture", confidence=0.82),
      KnowledgeItem(id=make_id("ki"), layer="INFERENCE", content=self._translate(language, "最初的解释框架会决定后续世界线的分叉角度。", "The first interpretation frame will determine how the worldline forks."), source_type="system", confidence=0.68),
      KnowledgeItem(id=make_id("ki"), layer="VALUE", content=self._translate(language, "系统会暴露谁承担代价，以及什么被视为可接受的损耗。", "The system exposes who absorbs the cost and what counts as acceptable loss."), source_type="system", confidence=0.73),
      KnowledgeItem(id=make_id("ki"), layer="ACTION", content=self._translate(language, "一次清晰但有代价的 intervention 会显著改变后续轨迹。", "A clear but costly intervention can noticeably bend the next trajectory."), source_type="system", confidence=0.76),
    ]

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
      knowledge_items=knowledge_items,
      confidence_updates=[
        ConfidenceUpdate(
          update_id=make_id("cu"),
          target_type="branch",
          target_id=primary_branch.branch_id,
          before=0.55,
          after=primary_branch.confidence,
          reason=self._translate(language, "多条早期信号在主分支上汇聚。", "Multiple early signals converge on the main branch."),
          method="rule",
          created_at=utc_now(),
        )
      ],
      replay_trace=[
        ReplayTraceItem(
          trace_id=make_id("rt"),
          event_id=key_events[0].event_id,
          event_title=key_events[0].title,
          branch_id=primary_branch.branch_id,
          branch_label=primary_branch.label,
          summary=self._translate(language, "主分支获得第一轮可见度优势。", "The primary branch gains the first visibility advantage."),
        )
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
    lead, rule, field, constraint = context.actants[:4]
    tertiary = context.actants[4] if len(context.actants) > 4 else field
    templates = [
      {
        "stage": self._translate(language, "入口", "Entry"),
        "impact": "high",
        "title": self._translate(language, f"{lead}进入可观测层", f"{lead} enters the observable layer"),
        "summary": self._translate(language, f"{context.seed_excerpt} 开始显影：{lead}、{rule} 与 {field} 被放进同一个作用场，世界线获得第一层方向。", f"{context.seed_excerpt} begins to appear: {lead}, {rule}, and {field} enter the same field, giving the worldline its first direction."),
        "affected": [lead, rule, field],
        "evidence": self._translate(language, f"Seed 线索把 {lead} 与 {rule} 同时推入场域。", f"The seed pushes {lead} and {rule} into the field together."),
        "causal": self._translate(language, "入口事件决定观众最先看见哪一层因果。", "The entry event decides which causal layer appears first."),
        "branches": [
          ("主轨显影", "Primary exposure", f"{lead}沿着{rule}快速获得方向，世界线可以立即推进。", f"{lead} gains direction through {rule}, allowing the worldline to advance immediately."),
          ("慢速校准", "Slow calibration", f"{field}先吸收不确定性，节点展开较慢但误伤更低。", f"{field} absorbs uncertainty first; the node unfolds slowly but with less collateral damage."),
          ("失控折叠", "Runaway fold", f"{constraint}被过早压缩，后续节点可能出现突然折叠。", f"{constraint} is compressed too early, creating a risk of sudden downstream folding."),
        ],
      },
      {
        "stage": self._translate(language, "折转", "Bend"),
        "impact": "medium",
        "title": self._translate(language, f"{constraint}重新分配轨道", f"{constraint} redistributes the track"),
        "summary": self._translate(language, f"{rule}、{constraint} 与 {tertiary} 开始争夺节奏：哪个对象先被保护，哪个对象先承压，会改变第二层分叉。", f"{rule}, {constraint}, and {tertiary} begin negotiating tempo: what gets protected first and what bears pressure first changes the second fork."),
        "affected": [rule, constraint, tertiary],
        "evidence": self._translate(language, f"{constraint}的压力正在转移到 {tertiary}。", f"Pressure from {constraint} is moving toward {tertiary}."),
        "causal": self._translate(language, "第一层显影形成的惯性开始改变资源与行动的顺序。", "The inertia from the first exposure changes the ordering of resources and actions."),
        "branches": [
          ("约束重排", "Constraint reallocation", f"系统承认{constraint}的存在，并把代价显式分摊到多个作用体。", f"The system acknowledges {constraint} and distributes cost across several actants."),
          ("局部绕行", "Local bypass", f"{tertiary}绕开主轨，保留一条较窄但更稳的路径。", f"{tertiary} bypasses the main track, preserving a narrower but steadier path."),
          ("材料断裂", "Material rupture", f"如果{rule}过度收紧，{field}会把压力变成可见断裂。", f"If {rule} tightens too hard, {field} turns pressure into visible rupture."),
        ],
      },
      {
        "stage": self._translate(language, "回响", "Ripple"),
        "impact": "medium",
        "title": self._translate(language, f"{field}沉积为新的世界残影", f"{field} settles into a new world afterimage"),
        "summary": self._translate(language, f"最后一层不会给出唯一答案，而是留下{lead}、{rule}、{constraint}之间的代价记录，作为下一轮观测和干涉的起点。", f"The last layer does not produce a single answer; it leaves a cost record among {lead}, {rule}, and {constraint} as the next starting point for observation and intervention."),
        "affected": [field, lead, constraint],
        "evidence": self._translate(language, f"{field}保留了前两层的弯折痕迹。", f"{field} retains the bends from the first two layers."),
        "causal": self._translate(language, "前两层选择沉积成新的边界条件。", "The first two layers settle into new boundary conditions."),
        "branches": [
          ("残影固化", "Afterimage settles", f"代价被记录下来，{lead}后续只能在新的边界内行动。", f"The cost is recorded; {lead} can only act within the new boundary."),
          ("重新开口", "Re-opened track", f"一次校准把{constraint}重新打开，让下一轮推演保留弹性。", f"A calibration reopens {constraint}, keeping the next simulation elastic."),
          ("长期回声", "Long echo", f"{field}把短期选择转化为更长的制度或环境回声。", f"{field} turns a short-term choice into a longer institutional or environmental echo."),
        ],
      },
    ]
    events: list[KeyEvent] = []
    previous_event_id = ""
    for index, template in enumerate(templates):
      event = self._event_from_template(world_state_id, language, index, previous_event_id, template)
      events.append(event)
      previous_event_id = event.event_id
    return events

  def _event_from_template(self, world_state_id: str, language: DisplayLanguage, index: int, previous_event_id: str, template: dict[str, Any]) -> KeyEvent:
    event_id = make_id("evt")
    confidences = [(0.64, 0.25, 0.11), (0.56, 0.29, 0.15), (0.51, 0.33, 0.16)][index]
    branches = [
      self._branch(event_id, language, template["branches"][0], confidences[0], "primary", "selected" if index == 0 else "candidate", "清晰度上升，但会把代价更快推给承压对象。", "Clarity rises, but cost moves faster onto pressured actants."),
      self._branch(event_id, language, template["branches"][1], confidences[1], "alternate", "candidate", "降低误伤，但会拉长不确定窗口。", "Reduces collateral damage but lengthens uncertainty."),
      self._branch(event_id, language, template["branches"][2], confidences[2], "alternate", "candidate", "可见度极高，但可能制造难以回收的后续损耗。", "Highly visible, but may create downstream damage that is hard to unwind."),
    ]
    return KeyEvent(
      event_id=event_id,
      world_state_id=world_state_id,
      title=template["title"],
      summary=template["summary"],
      depends_on_event_id=previous_event_id,
      causal_note=template["causal"],
      causal_strength="high" if index == 0 else "medium",
      collapse_hint=self._translate(language, "如果不推进，系统会停留在当前显影层。", "If not advanced, the system remains in the current exposure layer."),
      stage=template["stage"],
      impact_level=template["impact"],
      fold_state="expanded" if index == 0 else "collapsed",
      branches=branches,
      evidence_ids=[make_id("ev"), make_id("ev")],
      evidence_notes=[template["evidence"]],
      affected_entities=template["affected"],
    )

  def _branch(
    self,
    event_id: str,
    language: DisplayLanguage,
    labels: tuple[str, str, str, str],
    confidence: float,
    visibility: str,
    state: str,
    cost_zh: str,
    cost_en: str,
  ) -> Branch:
    zh_label, en_label, zh_description, en_description = labels
    return Branch(
      branch_id=make_id("br"),
      event_id=event_id,
      label=self._translate(language, zh_label, en_label),
      description=self._translate(language, zh_description, en_description),
      confidence=confidence,
      premises=[
        self._translate(language, "可观测材料已经足以支撑这一轨道继续显影。", "Observable material is sufficient for this track to keep appearing."),
        self._translate(language, "规则、环境和作用体之间存在稳定牵引。", "Rules, environments, and actants hold a stable pull."),
      ],
      signals_for=[
        self._translate(language, "因果链条开始对齐。", "The causal chain begins to align."),
        self._translate(language, "代价载体已经可见。", "The cost carrier is visible."),
      ],
      signals_against=[
        self._translate(language, "新的观测或修正仍可能改变证据层。", "A new observation or correction may still change the evidence layer."),
      ],
      visibility=visibility,  # type: ignore[arg-type]
      state=state,  # type: ignore[arg-type]
      cost_hint=self._translate(language, cost_zh, cost_en),
    )

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
      item = self._excerpt(str(value).strip(), 36)
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

  def _translate(self, language: DisplayLanguage, zh: str, en: str) -> str:
    return zh if language == "zh" else en

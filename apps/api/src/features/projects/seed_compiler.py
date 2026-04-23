from __future__ import annotations

from dataclasses import dataclass

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


class SeedCompiler:
  def __init__(self) -> None:
    self.llm_adapter = OpenAICompatibleLLMAdapter()

  def compile_fixture(self, fixture: dict, language: DisplayLanguage) -> ProjectSnapshot:
    project_id = make_id("proj")
    world_state_id = make_id("ws")
    session_id = make_id("sess")
    now = utc_now()
    title = self._translate(language, fixture["title"], fixture["title"])
    summary = self._translate(
      language,
      f"{fixture['summary']} 观众会在这条世界线里观察选择如何改变代价、共识与后果。",
      f"{fixture['summary']} The audience watches choices redistribute cost, legitimacy, and consequence.",
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
    llm_payload = self.llm_adapter.generate_json(
      operation="seed_compiler",
      language=language,
      payload={
        "task": "Build a short public-audience worldline seed",
        "seed_prompt": seed_prompt,
        "language": language,
      },
    )
    generated_title = seed_prompt.strip()[:60]
    generated_summary = seed_prompt.strip()
    seed_words = ["fragile consensus", "redistributed cost", "audience tension"]
    if llm_payload:
      generated_title = llm_payload.get("title") or generated_title
      generated_summary = llm_payload.get("summary") or generated_summary
      seed_words = llm_payload.get("seed_words") or seed_words
    title = self._translate(language, generated_title, generated_title)
    summary = self._translate(
      language,
      f"{generated_summary} 这个版本会优先生成可观察、可干预、可分享的公共世界线。",
      f"{generated_summary} This version prioritizes a public worldline that can be observed, bent, and shared.",
    )
    project = ProjectRecord(
      project_id=project_id,
      title=title,
      source_mode="seed_prompt",
      source_label="seed_prompt",
      seed_prompt=seed_prompt,
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
      seed_words=seed_words,
      source_label="seed_prompt",
      language=language,
    )
    return ProjectSnapshot(project=project, world_state=world_state)

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
      SourceEntity(entity_id=make_id("ent"), entity_kind="agent", name=self._translate(language, "发起者", "Initiator"), description=self._translate(language, "引发这条世界线的人与组织", "The people and groups that trigger the worldline.")),
      SourceEntity(entity_id=make_id("ent"), entity_kind="system", name=self._translate(language, "平台与制度", "Platforms and institutions"), description=self._translate(language, "决定可见度、节奏与阈值的系统外壳", "The systems that shape visibility, tempo, and thresholds.")),
      SourceEntity(entity_id=make_id("ent"), entity_kind="constraint", name=self._translate(language, "资源约束", "Resource pressure"), description=self._translate(language, "成本、时间与注意力限制", "Limits around cost, time, and attention.")),
      SourceEntity(entity_id=make_id("ent"), entity_kind="environment", name=self._translate(language, "公众气候", "Public climate"), description=self._translate(language, "观众情绪与社会背景场", "The social atmosphere surrounding the event.")),
    ]

    knowledge_items = [
      KnowledgeItem(id=make_id("ki"), layer="FACT", content=self._translate(language, "触发材料已经进入公共视野。", "The triggering material has entered public view."), source_type="fixture", confidence=0.82),
      KnowledgeItem(id=make_id("ki"), layer="INFERENCE", content=self._translate(language, "最初的解释框架会决定后续世界线的分叉角度。", "The first interpretation frame will determine how the worldline forks."), source_type="system", confidence=0.68),
      KnowledgeItem(id=make_id("ki"), layer="VALUE", content=self._translate(language, "人们会争论谁承担代价，以及什么被视为公平。", "People will argue about who absorbs the cost and what counts as fair."), source_type="system", confidence=0.73),
      KnowledgeItem(id=make_id("ki"), layer="ACTION", content=self._translate(language, "一次清晰但有代价的 intervention 会显著改变后续轨迹。", "A clear but costly intervention can noticeably bend the next trajectory."), source_type="system", confidence=0.76),
    ]

    key_events = self._build_events(world_state_id, language, seed_words)
    primary_branch = key_events[0].branches[0]
    share_artifact = ShareArtifact(
      title=title,
      subtitle=self._translate(language, "不是唯一未来，而是一张判断地图", "Not the only future, but a map of judgment"),
      summary=summary,
      disclaimer=self._translate(language, "这是一件可重演、可校准的判断作品，不是确定性预测。", "This is a replayable, calibratable judgment work, not a deterministic prediction."),
      share_text=self._translate(language, f"我进入了《{title}》的世界线，看到主分支如何形成，也看到选择会把代价转移给谁。", f"I stepped into the worldline of {title} and watched how the main branch forms while cost shifts between people."),
      tags=["miroworld", "worldline", "public-futures"],
      short_excerpt=self._translate(language, "世界线不是答案，它让代价发光。", "A worldline is not an answer. It makes the cost visible."),
      poster_caption=self._translate(language, "观察分支，承担选择。", "Observe the branch. Carry the choice."),
      curator_note=self._translate(language, "观众不是旁观者，而是变量。", "The audience is not a spectator, but a variable."),
      wall_label=self._translate(language, "一条由判断、误差与代价构成的公共世界线。", "A public worldline made of judgment, error, and cost."),
      archive_summary=self._translate(language, "第一版档案已经建立，后续 replay 与 calibration 会持续写入。", "The first archive is ready; later replays and calibrations will continue to write into it."),
    )

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
      share_context=self._translate(language, "公共体验 MVP", "Public experience MVP"),
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

  def _build_events(self, world_state_id: str, language: DisplayLanguage, seed_words: list[str]) -> list[KeyEvent]:
    templates = [
      {
        "title_zh": "触发材料进入公共视野",
        "title_en": "Trigger material enters public view",
        "summary_zh": "第一波观看、截图与解释开始塑造这条世界线的入口温度。",
        "summary_en": "The first wave of viewing, clipping, and framing shapes the entry temperature of the worldline.",
        "stage_zh": "入口",
        "stage_en": "Entry",
      },
      {
        "title_zh": "机构与平台开始重新分配位置",
        "title_en": "Institutions and platforms redistribute position",
        "summary_zh": "回应节奏、道歉方式与资源调度，决定公众会把谁放在代价中心。",
        "summary_en": "The response tempo, apology form, and resource routing decide who the public places at the center of cost.",
        "stage_zh": "扭转",
        "stage_en": "Bend",
      },
      {
        "title_zh": "后果沉淀为新的公众记忆",
        "title_en": "Consequences settle into new public memory",
        "summary_zh": "人们不只记住发生了什么，更记住谁承担、谁回避、谁被留下。",
        "summary_en": "People remember not only what happened, but who carried the burden, who avoided it, and who was left behind.",
        "stage_zh": "回响",
        "stage_en": "Ripple",
      },
    ]
    impact_levels = ["high", "medium", "medium"]
    confidences = [(0.66, 0.22, 0.12), (0.58, 0.27, 0.15), (0.52, 0.31, 0.17)]
    events: list[KeyEvent] = []
    for index, template in enumerate(templates):
      event_id = make_id("evt")
      stage = template["stage_zh"] if language == "zh" else template["stage_en"]
      branches = [
        Branch(
          branch_id=make_id("br"),
          event_id=event_id,
          label=self._translate(language, "主分支", "Primary branch"),
          description=self._translate(language, f"主线沿着“{seed_words[0] if seed_words else 'visible pressure'}”推进，世界线被重新定向。", f"The mainline advances through “{seed_words[0] if seed_words else 'visible pressure'}” and redirects the worldline."),
          confidence=confidences[index][0],
          premises=[
            self._translate(language, "最容易传播的解释先获得优势。", "The most transmissible interpretation gains the first advantage."),
            self._translate(language, "资源会先流向最能降低失控风险的动作。", "Resources flow first toward the action that reduces runaway risk."),
          ],
          signals_for=[
            self._translate(language, "平台排序与注意力密度同步增强。", "Platform ranking and attention density intensify together."),
            self._translate(language, "关键机构开始对齐话语。", "Key institutions begin aligning their language."),
          ],
          signals_against=[
            self._translate(language, "局部纠正可能重写证据层。", "A local correction could rewrite the evidence layer.")
          ],
          visibility="primary",
          state="selected" if index == 0 else "candidate",
          cost_hint=self._translate(language, "效率提升，但会把成本推向边缘群体。", "It improves clarity, but pushes cost onto edge groups."),
        ),
        Branch(
          branch_id=make_id("br"),
          event_id=event_id,
          label=self._translate(language, "替代分支", "Alternate branch"),
          description=self._translate(language, "如果更多反证进入现场，世界线会转向更慢但更复杂的协调路径。", "If more counter-signals enter the scene, the worldline bends toward a slower but richer coordination path."),
          confidence=confidences[index][1],
          premises=[
            self._translate(language, "观众仍保留判断弹性。", "The audience still retains judgment elasticity.")
          ],
          signals_for=[
            self._translate(language, "新的细节开始削弱单一叙事。", "New detail weakens the single narrative.")
          ],
          signals_against=[
            self._translate(language, "节奏过慢会被平台惩罚。", "A slow response may be punished by platform tempo.")
          ],
          visibility="alternate",
          state="candidate",
          cost_hint=self._translate(language, "能降低误伤，但会拖长不确定期。", "It reduces collateral damage but lengthens uncertainty."),
        ),
        Branch(
          branch_id=make_id("br"),
          event_id=event_id,
          label=self._translate(language, "高冲击低概率", "High-impact low-probability"),
          description=self._translate(language, "一次失控的误读或过强 intervention 可能让代价急剧集中。", "A runaway misreading or over-strong intervention could sharply concentrate the cost."),
          confidence=confidences[index][2],
          premises=[
            self._translate(language, "脆弱节点被过度放大。", "A fragile node gets over-amplified.")
          ],
          signals_for=[
            self._translate(language, "风险叙事开始压过事实层。", "Risk framing begins to dominate the fact layer.")
          ],
          signals_against=[
            self._translate(language, "稳定机构仍可吸收部分冲击。", "Stable institutions can still absorb part of the shock.")
          ],
          visibility="alternate",
          state="candidate",
          cost_hint=self._translate(language, "可见度极高，但会制造难以回收的后续损耗。", "Extremely visible, but creates downstream damage that is hard to unwind."),
        ),
      ]
      events.append(
        KeyEvent(
          event_id=event_id,
          world_state_id=world_state_id,
          title=template["title_zh"] if language == "zh" else template["title_en"],
          summary=template["summary_zh"] if language == "zh" else template["summary_en"],
          stage=stage,
          impact_level=impact_levels[index],
          fold_state="expanded" if index == 0 else "collapsed",
          branches=branches,
          evidence_ids=[make_id("ev"), make_id("ev")],
          evidence_notes=[
            self._translate(language, "事实层与价值层正在彼此牵引。", "The fact layer and value layer are already pulling on each other.")
          ],
          affected_entities=[
            self._translate(language, "发起者", "Initiator"),
            self._translate(language, "公众气候", "Public climate"),
          ],
          depends_on_event_id=events[-1].event_id if events else "",
          causal_note=self._translate(language, "上一阶段形成的解释惯性继续施压。", "The interpretive inertia from the previous stage keeps pressing forward."),
        )
      )
    return events

  def _build_cost_lenses(self, events: list[KeyEvent], language: DisplayLanguage) -> list[CostLens]:
    lenses: list[CostLens] = []
    for event in events:
      for branch in event.branches:
        lenses.append(
          CostLens(
            cost_lens_id=make_id("cl"),
            target_branch_id=branch.branch_id,
            first_order_costs=[
              self._translate(language, "注意力集中会压缩修正窗口。", "Attention concentration compresses the correction window."),
              self._translate(language, "执行速度上升会挤压共识缓冲区。", "Execution speed squeezes the buffer for consensus."),
            ],
            second_order_costs=[
              self._translate(language, "后续的信任修复会变得更慢、更贵。", "Later trust repair becomes slower and more expensive."),
              self._translate(language, "边缘群体承担的隐性代价会上升。", "Hidden costs borne by edge groups increase."),
            ],
            affected_groups=[
              self._translate(language, "被动承受者", "Passive bearers"),
              self._translate(language, "观察中的公众", "Watching public"),
            ],
            ethical_notes=[
              self._translate(language, "不要把清晰误认为正当。", "Do not mistake clarity for legitimacy."),
              self._translate(language, "低概率分支也可能包含最大道德代价。", "Low-probability branches may still contain the largest ethical burden."),
            ],
          )
        )
    return lenses

  def _translate(self, language: DisplayLanguage, zh: str, en: str) -> str:
    return zh if language == "zh" else en

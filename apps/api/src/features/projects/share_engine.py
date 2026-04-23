from __future__ import annotations

from .models import ShareArtifact, WorldState


class ShareEngine:
  def build(self, world_state: WorldState, language: str, *, event_id: str | None = None, branch_id: str | None = None) -> ShareArtifact:
    branch = self._resolve_branch(world_state, branch_id)
    title = world_state.headline
    if language == "zh":
      summary = f"{title} 正在沿着“{branch.label}”推进，观众能看到代价如何重新分配。"
      return ShareArtifact(
        title=title,
        subtitle="世界线不是答案，是代价的显影剂",
        summary=summary,
        disclaimer=world_state.disclaimer,
        share_text=f"我在 MiroWorld 里进入了《{title}》的世界线：{summary}",
        tags=["miroworld", "worldline", "cost"],
        short_excerpt="选择不仅改变方向，也改变谁来承担。",
        poster_caption="观察分支，承担选择。",
        curator_note="观众不是旁观者，而是世界线的变量。",
        wall_label=f"{title}：一条会因 intervention 与 correction 而偏折的公共世界线。",
        archive_summary=f"当前归档焦点：{branch.label}。",
      )
    summary = f"{title} is currently moving through '{branch.label}', making visible who absorbs the cost."
    return ShareArtifact(
      title=title,
      subtitle="A worldline is not an answer. It is a cost revealer.",
      summary=summary,
      disclaimer=world_state.disclaimer,
      share_text=f"I entered the worldline of {title} in MiroWorld: {summary}",
      tags=["miroworld", "worldline", "cost"],
      short_excerpt="Choices do not only change direction. They change who carries the burden.",
      poster_caption="Observe the branch. Carry the choice.",
      curator_note="The audience is not a spectator, but a variable inside the worldline.",
      wall_label=f"{title}: a public worldline that bends under intervention and correction.",
      archive_summary=f"Current archive focus: {branch.label}.",
    )

  def _resolve_branch(self, world_state: WorldState, branch_id: str | None):
    for event in world_state.key_events:
      for branch in event.branches:
        if branch.branch_id == branch_id:
          return branch
    return world_state.key_events[0].branches[0]

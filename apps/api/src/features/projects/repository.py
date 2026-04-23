from __future__ import annotations

import json

from config import get_settings
from core.errors import NotFoundError
from .models import ProjectSnapshot


class ProjectRepository:
  def __init__(self) -> None:
    self._root = get_settings().data_dir / "projects"

  def save(self, snapshot: ProjectSnapshot) -> ProjectSnapshot:
    target = self._root / f"{snapshot.project.project_id}.json"
    target.write_text(snapshot.model_dump_json(indent=2), encoding="utf-8")
    return snapshot

  def load(self, project_id: str) -> ProjectSnapshot:
    target = self._root / f"{project_id}.json"
    if not target.exists():
      raise NotFoundError(f"Project '{project_id}' was not found.")
    data = json.loads(target.read_text(encoding="utf-8"))
    return ProjectSnapshot.model_validate(data)

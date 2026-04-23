from __future__ import annotations

import json
from typing import Any

from config import get_settings
from core.errors import NotFoundError


class FixtureRepository:
  def __init__(self) -> None:
    self._root = get_settings().fixtures_dir

  def list_fixtures(self) -> dict[str, Any]:
    manifest = self._root / "manifest.json"
    return json.loads(manifest.read_text(encoding="utf-8"))

  def get_fixture(self, fixture_id: str) -> dict[str, Any]:
    manifest = self.list_fixtures()
    entry = next((item for item in manifest["fixtures"] if item["fixture_id"] == fixture_id), None)
    if not entry:
      raise NotFoundError(f"Fixture '{fixture_id}' was not found.")
    target = self._root / entry["file"]
    return json.loads(target.read_text(encoding="utf-8"))

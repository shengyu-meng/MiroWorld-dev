from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from config import get_settings
from shared.utils import stable_hash


class OpenAICompatibleLLMAdapter:
  def __init__(self) -> None:
    self.settings = get_settings()
    self.cache_dir = self.settings.data_dir / "cache"

  def _cache_path(self, key: str) -> Path:
    return self.cache_dir / f"{key}.json"

  def generate_json(
    self,
    *,
    operation: str,
    language: str,
    payload: dict[str, Any],
  ) -> dict[str, Any] | None:
    cache_key = stable_hash(json.dumps({
      "operation": operation,
      "language": language,
      "payload": payload,
    }, ensure_ascii=False, sort_keys=True))
    target = self._cache_path(cache_key)
    if target.exists():
      return json.loads(target.read_text(encoding="utf-8"))

    if not self.settings.llm_api_key:
      return None

    body = {
      "model": self.settings.llm_model_name,
      "messages": [
        {
          "role": "system",
          "content": (
            "Return one valid JSON object only. "
            "No markdown. No prose outside JSON."
          ),
        },
        {
          "role": "user",
          "content": json.dumps(payload, ensure_ascii=False),
        },
      ],
      "response_format": {"type": "json_object"},
      "temperature": 0.4,
    }

    headers = {
      "Authorization": f"Bearer {self.settings.llm_api_key}",
      "Content-Type": "application/json",
    }
    try:
      with httpx.Client(timeout=self.settings.llm_request_timeout) as client:
        response = client.post(
          f"{str(self.settings.llm_base_url).rstrip('/')}/chat/completions",
          headers=headers,
          json=body,
        )
        response.raise_for_status()
      content = response.json()["choices"][0]["message"]["content"]
      parsed = json.loads(content)
      target.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
      return parsed
    except Exception:
      return None

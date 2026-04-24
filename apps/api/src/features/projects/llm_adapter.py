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
    self.last_error: str | None = None

  def _cache_path(self, key: str) -> Path:
    return self.cache_dir / f"{key}.json"

  def generate_json(
    self,
    *,
    operation: str,
    language: str,
    payload: dict[str, Any],
  ) -> dict[str, Any] | None:
    self.last_error = None
    cache_key = stable_hash(json.dumps({
      "operation": operation,
      "language": language,
      "payload": payload,
    }, ensure_ascii=False, sort_keys=True))
    target = self._cache_path(cache_key)
    if target.exists():
      return json.loads(target.read_text(encoding="utf-8"))

    if not self.settings.llm_api_key:
      self.last_error = "missing LLM_API_KEY"
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
      parsed = self._parse_json_object(content)
      target.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
      return parsed
    except Exception as exc:
      self.last_error = self._safe_error(exc)
      return None

  def _parse_json_object(self, content: str) -> dict[str, Any]:
    """MiniMax reasoning models may prepend a <think> block before final JSON."""
    text = self._strip_think_block(content).strip()
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
      if char != "{":
        continue
      try:
        parsed, _end = decoder.raw_decode(text[index:])
      except json.JSONDecodeError:
        continue
      if isinstance(parsed, dict):
        return parsed
    raise ValueError("No JSON object found in LLM response.")

  def _strip_think_block(self, content: str) -> str:
    text = content.strip()
    lower = text.lower()
    closing = lower.rfind("</think>")
    if closing >= 0:
      return text[closing + len("</think>") :]
    opening = lower.find("<think>")
    if opening >= 0:
      first_json = text.find("{", opening)
      if first_json >= 0:
        return text[first_json:]
    return text

  def _safe_error(self, exc: Exception) -> str:
    message = f"{exc.__class__.__name__}: {exc}"
    if self.settings.llm_api_key:
      message = message.replace(self.settings.llm_api_key, "[redacted]")
    return message[:240]

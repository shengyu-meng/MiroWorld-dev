from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from uuid import uuid4


def utc_now() -> str:
  return datetime.now(timezone.utc).isoformat()


def make_id(prefix: str) -> str:
  return f"{prefix}_{uuid4().hex[:10]}"


def stable_hash(value: str) -> str:
  return hashlib.sha256(value.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
  cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
  return cleaned or "worldline"


def clamp(number: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
  return max(minimum, min(maximum, number))

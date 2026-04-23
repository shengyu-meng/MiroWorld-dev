from __future__ import annotations

from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    request_id = request.headers.get("x-request-id") or uuid4().hex[:12]
    request.state.request_id = request_id
    started_at = perf_counter()
    response = await call_next(request)
    duration_ms = round((perf_counter() - started_at) * 1000, 2)
    response.headers["x-request-id"] = request_id
    response.headers["x-response-time-ms"] = str(duration_ms)
    response.headers["x-content-type-options"] = "nosniff"
    response.headers["referrer-policy"] = "same-origin"
    response.headers["x-frame-options"] = "DENY"
    return response

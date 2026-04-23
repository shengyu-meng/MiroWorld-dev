from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
  status_code = 500
  code = "internal_error"

  def __init__(self, message: str, *, details: dict | None = None) -> None:
    super().__init__(message)
    self.message = message
    self.details = details or {}


class NotFoundError(AppError):
  status_code = 404
  code = "not_found"


class ValidationError(AppError):
  status_code = 422
  code = "validation_error"


class ConflictError(AppError):
  status_code = 409
  code = "conflict"


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
  return JSONResponse(
    status_code=exc.status_code,
    content={
      "success": False,
      "error": {
        "code": exc.code,
        "message": exc.message,
        "details": exc.details,
        "request_id": getattr(request.state, "request_id", ""),
      },
    },
  )

from __future__ import annotations

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import get_settings
from core.errors import AppError, app_error_handler
from core.logging import configure_logging
from core.middleware import RequestContextMiddleware
from features.fixtures.router import router as fixtures_router
from features.projects.router import router as projects_router
from features.system.router import router as system_router


configure_logging()
settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.app_debug)

app.add_middleware(RequestContextMiddleware)
app.add_middleware(
  CORSMiddleware,
  allow_origins=[settings.frontend_origin],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.exception_handler(AppError)
async def handle_app_error(request, exc):
  return await app_error_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request, exc):
  return JSONResponse(
    status_code=422,
    content={
      "success": False,
      "error": {
        "code": "request_validation_error",
        "message": "Request validation failed.",
        "details": exc.errors(),
        "request_id": getattr(request.state, "request_id", ""),
      },
    },
  )


app.include_router(system_router)
app.include_router(fixtures_router)
app.include_router(projects_router)

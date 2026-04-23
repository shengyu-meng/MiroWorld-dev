from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(tags=["system"])


@router.get("/health")
def health():
  return {
    "success": True,
    "data": {
      "status": "ok",
    },
  }


@router.get("/ready")
def ready():
  return {
    "success": True,
    "data": {
      "status": "ready",
    },
  }

from __future__ import annotations

from fastapi import APIRouter

from ..projects.service import ProjectService


router = APIRouter(prefix="/api/fixtures", tags=["fixtures"])
service = ProjectService()


@router.get("")
def list_fixtures():
  return {
    "success": True,
    "data": service.list_fixtures(),
  }

from __future__ import annotations

from fastapi import APIRouter

from .models import CalibrationRequest, InputRequest, ProjectCreateRequest, ShareRequest
from .service import ProjectService


router = APIRouter(prefix="/api/projects", tags=["projects"])
service = ProjectService()


@router.post("")
def create_project(payload: ProjectCreateRequest):
  snapshot = service.create_project(payload)
  return {
    "success": True,
    "data": {
      "project_id": snapshot.project.project_id,
      "stage": service.get_stage(snapshot.project.project_id, payload.language),
    },
  }


@router.get("/{project_id}/stage")
def get_stage(project_id: str, language: str = "zh"):
  return {
    "success": True,
    "data": service.get_stage(project_id, language),
  }


@router.post("/{project_id}/inputs")
def apply_input(project_id: str, payload: InputRequest):
  stage, replay_result = service.apply_input(project_id, payload)
  return {
    "success": True,
    "data": {
      "stage": stage,
      "replay_result": replay_result.model_dump(mode="json") if replay_result else None,
    },
  }


@router.post("/{project_id}/share")
def build_share(project_id: str, payload: ShareRequest):
  return {
    "success": True,
    "data": service.build_share(project_id, payload),
  }


@router.post("/{project_id}/calibration")
def record_calibration(project_id: str, payload: CalibrationRequest):
  return {
    "success": True,
    "data": service.record_calibration(project_id, payload),
  }

from __future__ import annotations

from fastapi import APIRouter

from .models import (
  CalibrationRequest,
  InputRequest,
  ProjectCreateRequest,
  ReplaySetSaveRequest,
  ShareRequest,
  TheatreProgressRequest,
)
from .service import ProjectService


router = APIRouter(prefix="/api/projects", tags=["projects"])
service = ProjectService()


@router.post("")
def create_project(payload: ProjectCreateRequest):
  snapshot, reasoning = service.create_project(payload)
  return {
    "success": True,
    "data": {
      "project_id": snapshot.project.project_id,
      "stage": service.get_stage(snapshot.project.project_id, payload.language),
      "reasoning": reasoning,
    },
  }


@router.get("/{project_id}/stage")
def get_stage(project_id: str, language: str = "zh"):
  return {
    "success": True,
    "data": service.get_stage(project_id, language),
  }


@router.get("/{project_id}/reasoning")
def get_reasoning_status(project_id: str, language: str = "zh"):
  return {
    "success": True,
    "data": service.get_reasoning_status(project_id, language),
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


@router.post("/{project_id}/progress")
def save_theatre_progress(project_id: str, payload: TheatreProgressRequest):
  return {
    "success": True,
    "data": service.save_theatre_progress(project_id, payload),
  }


@router.post("/{project_id}/replay-sets")
def save_replay_set(project_id: str, payload: ReplaySetSaveRequest):
  return {
    "success": True,
    "data": service.save_replay_set(project_id, payload),
  }


@router.delete("/{project_id}/replay-sets/{replay_set_id}")
def delete_replay_set(project_id: str, replay_set_id: str):
  return {
    "success": True,
    "data": service.delete_replay_set(project_id, replay_set_id),
  }

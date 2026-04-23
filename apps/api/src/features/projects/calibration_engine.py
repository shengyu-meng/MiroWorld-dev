from __future__ import annotations

from shared.utils import make_id, utc_now
from .models import CalibrationRecord, CalibrationRequest, WorldState


class CalibrationEngine:
  def record(self, world_state: WorldState, payload: CalibrationRequest) -> CalibrationRecord:
    record = CalibrationRecord(
      calibration_id=make_id("cal"),
      event_id=payload.event_id,
      branch_id=payload.branch_id,
      result=payload.result,
      actual_outcome=payload.actual_outcome,
      note=payload.note,
      created_at=utc_now(),
    )
    world_state.calibration_records.insert(0, record)
    world_state.updated_at = utc_now()
    return record

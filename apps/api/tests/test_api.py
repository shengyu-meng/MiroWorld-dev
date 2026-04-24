from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from main import app


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS_DIR = ROOT / "contracts"
client = TestClient(app)


def load_schema(name: str):
  schema = json.loads((CONTRACTS_DIR / name).read_text(encoding="utf-8"))
  registry = Registry()
  for target in CONTRACTS_DIR.glob("*.json"):
    candidate = json.loads(target.read_text(encoding="utf-8"))
    resource = Resource.from_contents(candidate)
    registry = registry.with_resource(candidate.get("$id", target.name), resource)
    registry = registry.with_resource(f"./{target.name}", resource)
  return Draft202012Validator(schema, registry=registry)


def assert_schema(name: str, payload):
  load_schema(name).validate(payload)


def assert_process_trace(stage):
  trace = stage["process_trace"]
  assert trace["storage_mode"] == "local_gitignored_runtime"
  assert len(trace["steps"]) == len(stage["observatory"]["key_events"])
  first_step = trace["steps"][0]
  assert {layer["layer"] for layer in first_step["layer_results"]} == {"FACT", "INFERENCE", "VALUE", "ACTION"}
  assert first_step["artifact_path"].startswith("data/runtime/process/")
  artifact_file = ROOT / first_step["artifact_path"]
  assert artifact_file.exists()


def create_fixture_project():
  response = client.post("/api/projects", json={"fixture_id": "literary-branching-world", "language": "zh"})
  assert response.status_code == 200
  return response.json()["data"]


def test_fixture_project_creation_and_stage_contracts():
  data = create_fixture_project()
  project_id = data["project_id"]
  assert_schema("stage-response.schema.json", data["stage"])
  assert_process_trace(data["stage"])

  stage_response = client.get(f"/api/projects/{project_id}/stage", params={"language": "zh"})
  assert stage_response.status_code == 200
  fetched_stage = stage_response.json()["data"]
  assert_schema("stage-response.schema.json", fetched_stage)
  assert_process_trace(fetched_stage)

  project_file = ROOT / "data" / "runtime" / "projects" / f"{project_id}.json"
  snapshot = json.loads(project_file.read_text(encoding="utf-8"))
  assert_schema("world-state.schema.json", snapshot["world_state"])


def test_prompt_project_creation():
  response = client.post("/api/projects", json={"seed_prompt": "A museum dispute fractures a city narrative.", "language": "en"})
  assert response.status_code == 200
  payload = response.json()["data"]
  assert payload["project_id"].startswith("proj_")
  assert_schema("stage-response.schema.json", payload["stage"])
  assert_process_trace(payload["stage"])


def test_theatre_progress_persistence_restores_stage_defaults():
  data = create_fixture_project()
  project_id = data["project_id"]
  stage = data["stage"]
  second_event = stage["observatory"]["key_events"][1]
  second_branch = second_event["branches"][0]

  progress_response = client.post(
    f"/api/projects/{project_id}/progress",
    json={
      "revealed_event_count": 2,
      "selected_event_id": second_event["event_id"],
      "selected_branch_id": second_branch["branch_id"],
      "active_surface": "ripple",
      "language": "zh",
    },
  )
  assert progress_response.status_code == 200
  progress = progress_response.json()["data"]
  assert progress["revealed_event_count"] == 2
  assert progress["selected_event_id"] == second_event["event_id"]
  assert progress["selected_branch_id"] == second_branch["branch_id"]
  assert progress["active_surface"] == "ripple"
  assert progress["updated_at"]

  stage_response = client.get(f"/api/projects/{project_id}/stage", params={"language": "zh"})
  assert stage_response.status_code == 200
  restored_stage = stage_response.json()["data"]
  assert_schema("stage-response.schema.json", restored_stage)
  assert restored_stage["surface_defaults"]["revealed_event_count"] == 2
  assert restored_stage["surface_defaults"]["selected_event_id"] == second_event["event_id"]
  assert restored_stage["surface_defaults"]["selected_branch_id"] == second_branch["branch_id"]
  assert restored_stage["surface_defaults"]["active_surface"] == "ripple"

  project_file = ROOT / "data" / "runtime" / "projects" / f"{project_id}.json"
  snapshot = json.loads(project_file.read_text(encoding="utf-8"))
  assert snapshot["world_state"]["theatre_progress"]["selected_event_id"] == second_event["event_id"]
  assert_schema("world-state.schema.json", snapshot["world_state"])


def test_input_replay_share_and_calibration_flow():
  payload = create_fixture_project()
  project_id = payload["project_id"]
  stage = payload["stage"]
  event_id = stage["surface_defaults"]["selected_event_id"]
  branch_id = stage["surface_defaults"]["selected_branch_id"]

  replay_response = client.post(
    f"/api/projects/{project_id}/inputs",
    json={
      "input_type": "intervention",
      "content": "Deploy a visible intervention.",
      "target_event_id": event_id,
      "target_branch_id": branch_id,
      "effect_scope": "world_state",
      "language": "zh",
    },
  )
  assert replay_response.status_code == 200
  replay_payload = replay_response.json()["data"]
  assert_schema("stage-response.schema.json", replay_payload["stage"])
  assert replay_payload["replay_result"] is not None
  assert_schema("replay-result.schema.json", replay_payload["replay_result"])

  share_response = client.post(
    f"/api/projects/{project_id}/share",
    json={"language": "zh", "event_id": event_id, "branch_id": branch_id},
  )
  assert share_response.status_code == 200
  assert_schema("share-artifact.schema.json", share_response.json()["data"])

  calibration_response = client.post(
    f"/api/projects/{project_id}/calibration",
    json={
      "event_id": event_id,
      "branch_id": branch_id,
      "result": "partial",
      "actual_outcome": "The audience split into two camps.",
      "note": "Recorded during smoke test.",
      "language": "zh",
    },
  )
  assert calibration_response.status_code == 200
  stage_payload = calibration_response.json()["data"]
  assert_schema("stage-response.schema.json", stage_payload)
  assert stage_payload["archive"]["calibration_summary"]["count"] >= 1


def test_replay_set_save_delete_and_stage_persistence():
  payload = create_fixture_project()
  project_id = payload["project_id"]
  stage = payload["stage"]
  event_id = stage["surface_defaults"]["selected_event_id"]
  branch_id = stage["surface_defaults"]["selected_branch_id"]
  event_title = stage["observatory"]["key_events"][0]["title"]
  branch_label = stage["observatory"]["key_events"][0]["branches"][0]["label"]
  replay_payload = {
    "replay_set_key": "current",
    "replay_set_label": "Current Set",
    "replay_set_note": "Tracks the currently selected path.",
    "authored_note": "A saved replay excerpt for persistence testing.",
    "artifact": {
      "title": "Current Set / Exhibit",
      "deck": "Deck line for the saved replay.",
      "wall_text": "Wall text for the saved replay.",
      "pressure_note": "Pressure note for the saved replay.",
      "closing_note": "Closing note for the saved replay.",
      "tags": ["Current Set", "Test"],
    },
    "focus": {
      "event_id": event_id,
      "event_title": event_title,
      "branch_id": branch_id,
      "branch_label": branch_label,
    },
    "metrics": {
      "event_count": 2,
      "average_confidence": 0.62,
      "average_pressure": 1.4,
      "alternate_count": 1,
    },
    "dossier": {
      "summary": "Saved replay dossier summary.",
      "entry": {
        "title": f"{event_title} / {branch_label}",
        "summary": "Entry summary.",
      },
      "hinge": {
        "title": f"{event_title} / {branch_label}",
        "summary": "Hinge summary.",
      },
      "terminal": {
        "title": f"{event_title} / {branch_label}",
        "summary": "Terminal summary.",
      },
    },
    "timeline": [
      {
        "index": "ARCHIVE 01",
        "stage": stage["observatory"]["key_events"][0]["stage"],
        "event_title": event_title,
        "branch_label": branch_label,
        "confidence": 0.62,
        "counter_signal_count": 1,
        "description": "Saved replay timeline entry.",
        "upstream": {
          "title": "Archive Origin",
          "summary": "Saved replay origin.",
        },
        "downstream": {
          "title": "Archive Open End",
          "summary": "Saved replay downstream.",
        },
        "focus": {
          "event_id": event_id,
          "event_title": event_title,
          "branch_id": branch_id,
          "branch_label": branch_label,
        },
      }
    ],
    "language": "zh",
  }

  save_response = client.post(
    f"/api/projects/{project_id}/replay-sets",
    json=replay_payload,
  )
  assert save_response.status_code == 200
  saved_payload = save_response.json()["data"]
  assert len(saved_payload) == 1
  assert saved_payload[0]["replay_set_key"] == "current"

  second_save_response = client.post(
    f"/api/projects/{project_id}/replay-sets",
    json={
      **replay_payload,
      "replay_set_label": "Current Set / Curated Variant",
      "replay_set_note": "A second authored reading of the same replay focus.",
      "artifact": {
        **replay_payload["artifact"],
        "title": "Current Set / Curated Variant / Exhibit",
      },
    },
  )
  assert second_save_response.status_code == 200
  second_saved_payload = second_save_response.json()["data"]
  assert len(second_saved_payload) == 2
  assert second_saved_payload[0]["replay_set_label"] == "Current Set / Curated Variant"
  assert second_saved_payload[1]["replay_set_label"] == "Current Set"

  stage_response = client.get(f"/api/projects/{project_id}/stage", params={"language": "zh"})
  assert stage_response.status_code == 200
  persisted_stage = stage_response.json()["data"]
  assert len(persisted_stage["ripple"]["saved_replay_sets"]) == 2
  assert persisted_stage["ripple"]["saved_replay_sets"][0]["replay_set_id"] == second_saved_payload[0]["replay_set_id"]

  delete_response = client.delete(
    f"/api/projects/{project_id}/replay-sets/{second_saved_payload[0]['replay_set_id']}",
  )
  assert delete_response.status_code == 200
  assert len(delete_response.json()["data"]) == 1


def test_invalid_effect_scope_is_rejected():
  payload = create_fixture_project()
  project_id = payload["project_id"]
  stage = payload["stage"]
  event_id = stage["surface_defaults"]["selected_event_id"]
  branch_id = stage["surface_defaults"]["selected_branch_id"]

  response = client.post(
    f"/api/projects/{project_id}/inputs",
    json={
      "input_type": "observation",
      "content": "This should not rewrite the world.",
      "target_event_id": event_id,
      "target_branch_id": branch_id,
      "effect_scope": "world_state",
      "language": "zh",
    },
  )
  assert response.status_code == 422
  assert response.json()["error"]["code"] == "validation_error"

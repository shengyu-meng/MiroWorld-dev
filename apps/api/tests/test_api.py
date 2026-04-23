from __future__ import annotations

import json
from pathlib import Path

import jsonschema
from fastapi.testclient import TestClient

from main import app


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS_DIR = ROOT / "contracts"
client = TestClient(app)


def load_schema(name: str):
  schema = json.loads((CONTRACTS_DIR / name).read_text(encoding="utf-8"))
  store = {}
  for target in CONTRACTS_DIR.glob("*.json"):
    candidate = json.loads(target.read_text(encoding="utf-8"))
    store[candidate.get("$id", target.name)] = candidate
    store[f"./{target.name}"] = candidate
  resolver = jsonschema.RefResolver.from_schema(schema, store=store)
  return schema, resolver


def assert_schema(name: str, payload):
  schema, resolver = load_schema(name)
  jsonschema.validate(payload, schema, resolver=resolver)


def create_fixture_project():
  response = client.post("/api/projects", json={"fixture_id": "literary-branching-world", "language": "zh"})
  assert response.status_code == 200
  return response.json()["data"]


def test_fixture_project_creation_and_stage_contracts():
  data = create_fixture_project()
  project_id = data["project_id"]
  assert_schema("stage-response.schema.json", data["stage"])

  stage_response = client.get(f"/api/projects/{project_id}/stage", params={"language": "zh"})
  assert stage_response.status_code == 200
  assert_schema("stage-response.schema.json", stage_response.json()["data"])

  project_file = ROOT / "data" / "runtime" / "projects" / f"{project_id}.json"
  snapshot = json.loads(project_file.read_text(encoding="utf-8"))
  assert_schema("world-state.schema.json", snapshot["world_state"])


def test_prompt_project_creation():
  response = client.post("/api/projects", json={"seed_prompt": "A museum dispute fractures a city narrative.", "language": "en"})
  assert response.status_code == 200
  payload = response.json()["data"]
  assert payload["project_id"].startswith("proj_")
  assert_schema("stage-response.schema.json", payload["stage"])


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

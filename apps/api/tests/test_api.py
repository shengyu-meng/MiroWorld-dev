from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from main import app
from features.projects.llm_adapter import OpenAICompatibleLLMAdapter
from features.projects.reasoning_jobs import ReasoningJobManager
from features.projects.router import service as project_service
from features.projects.seed_compiler import SeedCompiler


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


def test_prompt_project_creation(monkeypatch):
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_seed_compiler_enabled", False)
  prompt = "A bridge load rule changes overnight; tide, steel, and commuter paths begin pulling on each other."
  response = client.post("/api/projects", json={"seed_prompt": prompt, "language": "en"})
  assert response.status_code == 200
  payload = response.json()["data"]
  assert payload["project_id"].startswith("proj_")
  assert_schema("stage-response.schema.json", payload["stage"])
  assert_process_trace(payload["stage"])
  stage = payload["stage"]
  event_blob = " ".join(
    f"{event['title']} {event['summary']} {' '.join(event['affected_entities'])}"
    for event in stage["observatory"]["key_events"]
  ).lower()
  assert "bridge" in event_blob
  assert "tide" in stage["project_context"]["summary"].lower()
  assert "museum dispute" not in event_blob
  assert len(stage["observatory"]["key_events"]) == 3
  assert all(len(event["branches"]) >= 3 for event in stage["observatory"]["key_events"])


def fake_llm_reasoning_packet():
  return {
    "title": "Bridge Tide Shear",
    "summary": "A bridge, tide, steel fatigue, and commuter pressure form a coupled worldline.",
    "seed_words": ["bridge load", "tide", "steel fatigue", "commuter path"],
    "actants": ["bridge deck", "tide table", "steel cable", "commuter route"],
    "reasoning_steps": [
      {
        "layer": "FACT",
        "title": "Visible coupling",
        "inputs": ["bridge load", "tide"],
        "outputs": ["tide changes load timing"],
        "confidence_note": "seed-level inference",
        "confidence": 0.81,
      }
    ],
    "events": [
      {
        "stage": "Entry",
        "title": "Tide enters the bridge load field",
        "summary": "The tide table changes how the bridge deck receives pressure.",
        "impact_level": "high",
        "affected_entities": ["bridge deck", "tide table"],
        "evidence_notes": ["load timing and water level become coupled"],
        "causal_note": "The rule change makes the coupling visible.",
        "branches": [
          {
            "label": "Expose the load rhythm",
            "description": "Make the tide-load relation observable.",
            "confidence": 0.69,
            "premises": ["water level modulates stress"],
            "signals_for": ["commuter peaks align with tide"],
            "signals_against": ["steel fatigue remains uncertain"],
            "cost_hint": "inspection slows traffic",
          }
        ],
      }
    ],
  }


def test_prompt_project_creation_queues_backstage_reasoning(monkeypatch):
  manager = ReasoningJobManager(provider="MiniMax", model_name="MiniMax-M2.7-highspeed")
  manager.auto_start = False
  monkeypatch.setattr(project_service, "reasoning_jobs", manager)
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_seed_compiler_enabled", True)
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_api_key", "test-local-key")
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_model_name", "MiniMax-M2.7-highspeed")

  calls = {"count": 0}

  def fake_generate(**_kwargs):
    calls["count"] += 1
    return fake_llm_reasoning_packet()

  monkeypatch.setattr(project_service.seed_compiler.llm_adapter, "generate_json", fake_generate)
  response = client.post(
    "/api/projects",
    json={
      "seed_prompt": "A bridge load rule changes overnight; tide and commuter paths begin pulling on each other.",
      "language": "en",
    },
  )
  assert response.status_code == 200
  payload = response.json()["data"]
  assert payload["reasoning"]["status"] == "queued"
  assert payload["stage"]["project_context"]["source_label"] == "seed_prompt"
  assert payload["stage"]["process_trace"]["reasoning_run"] is None
  assert calls["count"] == 0

  status_response = client.get(f"/api/projects/{payload['project_id']}/reasoning", params={"language": "en"})
  assert status_response.status_code == 200
  status_payload = status_response.json()["data"]
  assert_schema("reasoning-status.schema.json", status_payload)
  assert status_payload["status"] == "queued"
  assert status_payload["stage"] is None


def test_backstage_reasoning_merges_completed_packet(monkeypatch):
  manager = ReasoningJobManager(provider="MiniMax", model_name="MiniMax-M2.7-highspeed")
  manager.auto_start = False
  monkeypatch.setattr(project_service, "reasoning_jobs", manager)
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_seed_compiler_enabled", True)
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_api_key", "test-local-key")
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_model_name", "MiniMax-M2.7-highspeed")
  monkeypatch.setattr(
    project_service.seed_compiler.llm_adapter,
    "generate_json",
    lambda **_kwargs: fake_llm_reasoning_packet(),
  )
  create_response = client.post(
    "/api/projects",
    json={
      "seed_prompt": "A bridge load rule changes overnight; tide and commuter paths begin pulling on each other.",
      "language": "en",
    },
  )
  project_id = create_response.json()["data"]["project_id"]
  manager.run_queued_for_tests(project_id)

  status_response = client.get(f"/api/projects/{project_id}/reasoning", params={"language": "en"})
  assert status_response.status_code == 200
  status_payload = status_response.json()["data"]
  assert_schema("reasoning-status.schema.json", status_payload)
  assert status_payload["status"] == "completed"
  assert status_payload["artifact_path"].endswith("00-minimax-seed-reasoning.json")
  assert status_payload["stage"]["project_context"]["source_label"] == "seed_prompt+MiniMax"
  assert status_payload["stage"]["process_trace"]["reasoning_run"]["status"] == "completed"
  assert "Tide enters" in status_payload["stage"]["observatory"]["key_events"][0]["title"]


def test_backstage_reasoning_records_fallback_without_leaking_key(monkeypatch):
  manager = ReasoningJobManager(provider="MiniMax", model_name="MiniMax-M2.7-highspeed")
  manager.auto_start = False
  monkeypatch.setattr(project_service, "reasoning_jobs", manager)
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_seed_compiler_enabled", True)
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_api_key", "test-local-key")
  monkeypatch.setattr(project_service.seed_compiler.llm_adapter.settings, "llm_model_name", "MiniMax-M2.7-highspeed")

  def fail_generation(**_kwargs):
    project_service.seed_compiler.llm_adapter.last_error = "TimeoutException: request timed out"
    return None

  monkeypatch.setattr(project_service.seed_compiler.llm_adapter, "generate_json", fail_generation)
  create_response = client.post(
    "/api/projects",
    json={
      "seed_prompt": "A storm surge pushes hospital power and harbor timing into one track.",
      "language": "en",
    },
  )
  project_id = create_response.json()["data"]["project_id"]
  manager.run_queued_for_tests(project_id)
  status_payload = client.get(f"/api/projects/{project_id}/reasoning", params={"language": "en"}).json()["data"]
  assert_schema("reasoning-status.schema.json", status_payload)
  assert status_payload["status"] == "fallback"
  assert status_payload["artifact_path"].endswith("00-minimax-seed-fallback.json")
  artifact = json.loads((ROOT / status_payload["artifact_path"]).read_text(encoding="utf-8"))
  assert "test-local-key" not in json.dumps(artifact)


def test_llm_adapter_extracts_json_after_think_block():
  adapter = OpenAICompatibleLLMAdapter()
  parsed = adapter._parse_json_object('<think>private reasoning {"noise": true}</think> {"ok": true, "value": 3}')
  assert parsed == {"ok": True, "value": 3}


def test_prompt_compiler_can_run_without_live_llm_when_disabled(monkeypatch):
  compiler = SeedCompiler()
  monkeypatch.setattr(compiler.llm_adapter.settings, "llm_seed_compiler_enabled", False)

  def fail_if_called(**_kwargs):
    raise AssertionError("Prompt creation must not block on a live LLM call by default.")

  monkeypatch.setattr(compiler.llm_adapter, "generate_json", fail_if_called)
  snapshot = compiler.compile_prompt(
    "A glacier, a ferry timetable, and a municipal rule begin pulling the same route.",
    "en",
  )
  assert snapshot.project.source_mode == "seed_prompt"
  assert len(snapshot.world_state.key_events) == 3
  assert "glacier" in snapshot.world_state.key_events[0].title.lower()


def test_prompt_compiler_uses_structured_llm_reasoning_packet(monkeypatch):
  compiler = SeedCompiler()
  monkeypatch.setattr(compiler.llm_adapter.settings, "llm_seed_compiler_enabled", True)
  monkeypatch.setattr(compiler.llm_adapter.settings, "llm_model_name", "MiniMax-M2.7-highspeed")
  monkeypatch.setattr(
    compiler.llm_adapter,
    "generate_json",
    lambda **_kwargs: {
      "title": "Bridge Tide Shear",
      "summary": "A bridge, tide, steel fatigue, and commuter pressure form a coupled worldline.",
      "seed_words": ["bridge load", "tide", "steel fatigue", "commuter path"],
      "actants": ["bridge deck", "tide table", "steel cable", "commuter route"],
      "reasoning_steps": [
        {
          "layer": "FACT",
          "title": "Visible coupling",
          "inputs": ["bridge load", "tide"],
          "outputs": ["tide changes load timing"],
          "confidence_note": "seed-level inference",
          "confidence": 0.81,
        }
      ],
      "events": [
        {
          "stage": "Entry",
          "title": "Tide enters the bridge load field",
          "summary": "The tide table changes how the bridge deck receives pressure.",
          "impact_level": "high",
          "affected_entities": ["bridge deck", "tide table"],
          "evidence_notes": ["load timing and water level become coupled"],
          "causal_note": "The rule change makes the coupling visible.",
          "branches": [
            {
              "label": "Expose the load rhythm",
              "description": "Make the tide-load relation observable.",
              "confidence": 0.69,
              "premises": ["water level modulates stress"],
              "signals_for": ["commuter peaks align with tide"],
              "signals_against": ["steel fatigue remains uncertain"],
              "cost_hint": "inspection slows traffic",
            }
          ],
        }
      ],
    },
  )
  snapshot = compiler.compile_prompt(
    "A bridge load rule changes overnight; tide, steel, and commuter paths begin pulling on each other.",
    "en",
  )
  assert snapshot.world_state.source_label == "seed_prompt+MiniMax"
  assert snapshot.world_state.reasoning_runs[0].model_name == "MiniMax-M2.7-highspeed"
  assert snapshot.world_state.reasoning_runs[0].artifact_path.startswith("data/runtime/process/")
  assert "Tide enters" in snapshot.world_state.key_events[0].title
  assert snapshot.world_state.knowledge_items[0].source_type == "minimax_reasoning"


def test_prompt_compiler_records_failed_llm_attempt(monkeypatch):
  compiler = SeedCompiler()
  monkeypatch.setattr(compiler.llm_adapter.settings, "llm_seed_compiler_enabled", True)
  monkeypatch.setattr(compiler.llm_adapter.settings, "llm_api_key", "test-local-key")
  monkeypatch.setattr(compiler.llm_adapter.settings, "llm_model_name", "MiniMax-M2.7-highspeed")

  def fail_generation(**_kwargs):
    compiler.llm_adapter.last_error = "TimeoutException: request timed out"
    return None

  monkeypatch.setattr(compiler.llm_adapter, "generate_json", fail_generation)
  snapshot = compiler.compile_prompt(
    "A slow storm surge pushes hospital power, a harbor gate, and evacuation timing into one track.",
    "en",
  )
  run = snapshot.world_state.reasoning_runs[0]
  artifact_file = ROOT / run.artifact_path
  artifact = json.loads(artifact_file.read_text(encoding="utf-8"))

  assert snapshot.world_state.source_label == "seed_prompt"
  assert run.status == "fallback"
  assert run.step_count == 0
  assert run.artifact_path.endswith("00-minimax-seed-fallback.json")
  assert artifact["status"] == "fallback"
  assert "test-local-key" not in json.dumps(artifact)


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

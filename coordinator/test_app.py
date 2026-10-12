from fastapi.testclient import TestClient
import app as coordinator

client = TestClient(coordinator.app)

def test_health_endpoint_is_available_without_model_credentials():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "plan_only"}

def test_task_validation_rejects_short_task():
    response = client.post("/tasks", json={"task": "short", "mode": "plan_only"})
    assert response.status_code == 422

def test_task_requires_plan_only_mode():
    response = client.post("/tasks", json={"task": "Please inspect this example application", "mode": "execute"})
    assert response.status_code == 422

def test_missing_api_key_fails_closed(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "")
    response = client.post(
        "/tasks",
        json={"task": "Review a toy application and suggest a safe minimal repair plan.", "mode": "plan_only"},
    )
    assert response.status_code == 503
    assert "OPENAI_API_KEY is missing" in response.json()["detail"]

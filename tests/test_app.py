# tests/test_app.py
#
# WHY THIS FILE EXISTS:
# Automated tests are what make CI/CD pipelines meaningful. Without
# tests, Jenkins/GitHub Actions just "builds and ships" — with tests,
# it can actually BLOCK a bad deployment before it reaches production.
#
# WHERE THIS IS USED IN COMPANIES:
# Every CI pipeline has a "test" stage. If tests fail, the pipeline
# stops immediately — the build never reaches Docker/Kubernetes.
# This is often the FIRST quality gate in a real pipeline.

import os
import pytest

# Use a separate throwaway test database so we never touch real data
os.environ["DB_PATH"] = "test_tasks.db"
os.environ["APP_ENV"] = "testing"

from app.main import create_app  # noqa: E402


@pytest.fixture
def client():
    """
    Pytest fixture: runs before each test function that uses it.
    Creates a fresh Flask test client connected to a clean test DB.
    """
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

    # Cleanup: remove the test database file after each test
    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == {"tasks": []}


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Learn Docker"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Learn Docker"
    assert data["done"] == 0


def test_create_task_missing_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400


def test_mark_task_done(client):
    create_resp = client.post("/tasks", json={"title": "Deploy app"})
    task_id = create_resp.get_json()["id"]

    update_resp = client.put(f"/tasks/{task_id}", json={"done": True})
    assert update_resp.status_code == 200
    assert update_resp.get_json()["done"] == 1


def test_delete_task(client):
    create_resp = client.post("/tasks", json={"title": "Temp task"})
    task_id = create_resp.get_json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_get_nonexistent_task(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404

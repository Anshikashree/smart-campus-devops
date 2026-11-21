import os
import sys
import importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def load_test_app(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    import app as application_module
    importlib.reload(application_module)
    return application_module.app


def test_home_and_health(tmp_path, monkeypatch):
    app = load_test_app(tmp_path, monkeypatch)
    client = app.test_client()
    assert client.get("/").status_code == 200
    assert client.get("/health").json["status"] == "healthy"


def test_register_and_list(tmp_path, monkeypatch):
    app = load_test_app(tmp_path, monkeypatch)
    client = app.test_client()
    response = client.post("/api/students", json={"name":"Test User","email":"test@example.com","course":"Data Science"})
    assert response.status_code == 201
    assert client.get("/api/students").json[0]["name"] == "Test User"


def test_validation_and_duplicate(tmp_path, monkeypatch):
    app = load_test_app(tmp_path, monkeypatch)
    client = app.test_client()
    assert client.post("/api/students", json={"name":"","email":"","course":""}).status_code == 400
    payload = {"name":"Test User","email":"dup@example.com","course":"DS"}
    assert client.post("/api/students", json=payload).status_code == 201
    assert client.post("/api/students", json=payload).status_code == 409

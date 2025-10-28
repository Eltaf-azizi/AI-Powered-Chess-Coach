# tests/test_backend.py
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("ok") is True


def test_start_and_state():
    r = client.post("/game/start", json={"mode":"local"})
    assert r.status_code == 200
    data = r.json()
    assert "game_id" in data
    game_id = data["game_id"]

    r2 = client.get(f"/game/state/{game_id}")
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["game_id"] == game_id

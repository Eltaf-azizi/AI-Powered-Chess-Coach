# tests/test_integration.py
from fastapi.testclient import TestClient
from backend.app import app
import chess

client = TestClient(app)


def test_move_flow():
    # start game
    r = client.post("/game/start", json={"mode":"local"})
    assert r.status_code == 200
    gid = r.json()["game_id"]

    # make legal move e2e4
    move = "e2e4"
    r2 = client.post("/game/move", json={"game_id": gid, "uci": move})
    assert r2.status_code == 200
    data = r2.json()
    assert "analysis" in data
    assert data["fen"] is not None

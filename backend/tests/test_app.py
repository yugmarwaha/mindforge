import json
from pathlib import Path

import pytest

from app import create_app


@pytest.fixture
def client(tmp_path: Path):
    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "2026-04-13.json").write_text(
        json.dumps(
            {
                "date": "2026-04-13",
                "theme": "kitchen",
                "target_word": "KNIFE",
                "generated_by": "test-fixture",
            }
        )
    )
    app = create_app()
    app.config.update(
        TESTING=True,
        PUZZLES_DIR=str(tmp_path),
        EXAMPLES_DIR=str(examples),
    )
    return app.test_client()


def test_puzzle_today_hides_target_word(client):
    resp = client.get("/api/puzzle/today")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == {"date": "2026-04-13", "theme": "kitchen", "reveal_length": 5}
    assert "target_word" not in data


def test_guess_wrong_then_correct(client):
    wrong = client.post("/api/guess", json={"guess": "world"})
    assert wrong.status_code == 200
    body = wrong.get_json()
    assert body["solved"] is False
    assert body["guess_count"] == 1
    assert len(body["feedback"]) == 5

    right = client.post("/api/guess", json={"guess": "knife"})
    assert right.status_code == 200
    body = right.get_json()
    assert body["solved"] is True
    assert body["guess_count"] == 2
    assert body["feedback"] == ["hit"] * 5


def test_invalid_guess_returns_400(client):
    resp = client.post("/api/guess", json={"guess": "hi"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_missing_guess_field_returns_400(client):
    resp = client.post("/api/guess", json={})
    assert resp.status_code == 400


def test_guess_after_solve_returns_409(client):
    client.post("/api/guess", json={"guess": "knife"})
    resp = client.post("/api/guess", json={"guess": "world"})
    assert resp.status_code == 409

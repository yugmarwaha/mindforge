from __future__ import annotations

import json
import os
import secrets
from datetime import date
from pathlib import Path

from flask import Flask, abort, jsonify, request, session

from game.state import GameOverError, GameState
from game.validate import InvalidGuessError

BASE_DIR = Path(__file__).parent


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "MINDFORGE_SECRET", "dev-only-secret-do-not-ship"
    )
    app.config["PUZZLES_DIR"] = str(BASE_DIR / "puzzles")
    app.config["EXAMPLES_DIR"] = str(BASE_DIR / "puzzles" / "examples")

    # In-memory per-session game state: {sid: GameState}.
    # Cleared on server restart; Phase 1 is a single-player local app.
    app.extensions["mindforge_sessions"] = {}

    def today_str() -> str:
        return date.today().isoformat()

    def load_puzzle() -> dict:
        puzzles_dir = Path(app.config["PUZZLES_DIR"])
        examples_dir = Path(app.config["EXAMPLES_DIR"])
        d = today_str()
        for path in (puzzles_dir / f"{d}.json", examples_dir / f"{d}.json"):
            if path.exists():
                return json.loads(path.read_text())
        examples = sorted(examples_dir.glob("*.json")) if examples_dir.exists() else []
        if examples:
            return json.loads(examples[0].read_text())
        abort(503, description="no puzzle available")

    def get_or_create_state() -> GameState:
        puzzle = load_puzzle()
        sid = session.get("sid")
        if sid is None:
            sid = secrets.token_urlsafe(16)
            session["sid"] = sid
        sessions = app.extensions["mindforge_sessions"]
        state = sessions.get(sid)
        if state is None or session.get("puzzle_date") != puzzle["date"]:
            state = GameState(target=puzzle["target_word"])
            sessions[sid] = state
            session["puzzle_date"] = puzzle["date"]
        return state

    @app.get("/api/puzzle/today")
    def puzzle_today():
        puzzle = load_puzzle()
        return jsonify(
            {
                "date": puzzle["date"],
                "theme": puzzle["theme"],
                "reveal_length": len(puzzle["target_word"]),
            }
        )

    @app.post("/api/guess")
    def submit_guess():
        data = request.get_json(silent=True) or {}
        guess = data.get("guess")
        if not isinstance(guess, str):
            return jsonify({"error": "guess must be a string"}), 400
        state = get_or_create_state()
        try:
            result = state.guess(guess)
        except InvalidGuessError as e:
            return jsonify({"error": str(e)}), 400
        except GameOverError as e:
            return jsonify({"error": str(e)}), 409
        return jsonify(
            {
                "feedback": result.feedback,
                "solved": result.solved,
                "guess_count": result.guess_count,
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)

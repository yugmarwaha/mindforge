# Mindforge

## Project purpose
A themed daily Wordle. Each day's puzzle is produced by agentic puzzle generation — words are chosen around a hidden theme that the solver discovers alongside the letters.

## Tech stack
- **Backend:** Python 3.14, Flask, pip for dependency management
- **Frontend:** React via Vite (no Create-React-App; always Vite). JavaScript, not TypeScript, for now.
- **Dev:** two servers during development — Flask on port 5000, Vite on 5173. Vite proxies `/api/*` to Flask.
- **Prod:** Flask serves the built Vite bundle as static files from `frontend/dist/`.

## Folder conventions
- `backend/` — Flask app
  - `backend/app.py` — entrypoint, routes
  - `backend/game/` — pure-python Wordle game logic (state, guess validation). No Flask imports here.
  - `backend/puzzles/` — generated daily puzzle JSON files
  - `backend/tests/` — pytest
- `frontend/` — Vite + React app
  - `frontend/src/` — components, styles
  - `frontend/dist/` — build output (gitignored)
- `scripts/` — one-off scripts (e.g., regenerate today's puzzle)
- `history/` — gitignored; per-player game history
- `.claude/agents/` — subagent definitions

## Rules
- **Never generate the daily word directly.** Always route word/puzzle generation through the `puzzle-generator` subagent.
- **Never commit anything in `backend/puzzles/` except the `examples/` subfolder.** Real daily puzzles are answers — we don't leak them in the public repo.
- **Keep `backend/game/` framework-free.** No Flask, no request objects. Pure logic, testable with pytest.
- **Ask before installing any new pip package.** Keep dependencies minimal.

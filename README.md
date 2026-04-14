# Mindforge

Mindforge is a themed daily Wordle where every day's puzzle is crafted by an AI agent around a hidden theme. Instead of five random letters, each guess nudges you toward both the word and the connection linking it to the rest of the day's set — a small daily exercise in pattern-finding.

## Stack

- Python 3.14 + Flask 3 (backend)
- React 19 + Vite 8, JavaScript (frontend)
- Flat JSON puzzle files in `backend/puzzles/`
- No database; player history lives in browser `localStorage`

## Setup

```bash
# Python deps (create the venv yourself, then):
source .venv/bin/activate
pip install -r requirements.txt

# Frontend deps
npm install --prefix frontend
```

## Run

Two terminals, both from the project root.

**Backend — Flask on http://localhost:5000**
```bash
source .venv/bin/activate
python backend/app.py
```

**Frontend — Vite on http://localhost:5173**
```bash
npm run dev --prefix frontend
```

Open http://localhost:5173/. Vite proxies `/api/*` to Flask so session cookies stay same-origin and there's no CORS config to manage.

The repo ships a demo puzzle (`backend/puzzles/examples/2026-04-13.json`) so everything works without the agent pipeline running.

## Test

```bash
# Backend: 39 pytest cases covering game logic + the Flask routes
pytest backend/tests/

# Frontend: lint + production build
npm run lint --prefix frontend
npm run build --prefix frontend
```

## Layout

```
backend/
  app.py                # Flask entrypoint, API routes
  game/                 # Pure-Python Wordle core, no Flask imports
    state.py            # GameState dataclass
    validate.py         # Guess validation + feedback
  puzzles/examples/     # Committed demo puzzles
  tests/                # pytest
frontend/
  src/
    App.jsx             # Game orchestrator (fetch, guess, localStorage)
    components/         # Grid, Keyboard, ThemeBanner
    styles.css
  vite.config.js        # /api proxy to Flask
scripts/                # Agent-pipeline orchestrator (Phase 1 step 6, TBD)
.claude/agents/         # Subagent specs (Phase 1 step 5, TBD)
```

## Deployment note

The Flask session signing key falls back to a hardcoded dev placeholder when `MINDFORGE_SECRET` isn't set. Before deploying anywhere non-local, export a real random secret and do not commit it:

```bash
export MINDFORGE_SECRET="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

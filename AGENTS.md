# AGENTS.md

Spendly — a small Flask personal finance tracker. This is a step-by-step student project: many routes and the DB layer are intentionally left as placeholders to be implemented in later steps. Don't "fix" them unless asked.

## Run / test
- Run the app: `venv\Scripts\python.exe app.py` (Windows venv). Dev server runs `debug=True` on port **5001** (not the default 5000).
- No tests exist yet; `pytest` + `pytest-flask` are in `requirements.txt` for future steps.

## Structure
- `app.py` — entry point and all routes. Page routes `render_template(...)`; others (`logout`, `profile`, `expenses/...`) return placeholder strings.
- `database/db.py` — stub. Later steps add `get_db()`, `init_db()`, `seed_db()` (SQLite). `expense_tracker.db` is gitignored.
- `templates/` — all pages `{% extends "base.html" %}`; override blocks `title`, `head`, `content`, `scripts`. Use `url_for()` for links/static, never hardcoded paths.

## Conventions
- Vanilla JS only — no frameworks or libraries (explicit project constraint).
- Commit messages use lowercase conventional style: `landing: add privacy policy page and route`.
- `file.md`/`file.txt` in the repo root are scratch notes (stale), not authoritative docs.
- No lint/typecheck configured.
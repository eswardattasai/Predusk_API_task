# Contributing

Thanks for improving this portfolio API!

## Setup
1) Create venv and install:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
```
2) Seed local DB:
```bash
PYTHONPATH=backend python -c "from app.seed import run; run()"
```

## Dev commands
- `make run` – run FastAPI
- `make ui` – run static frontend
- `make seed` – reseed if DB empty
- `make check` – basic CI checks

## Code style
- Keep endpoints small and documented in `docs/API.md`.
- Prefer idempotent seed and explicit migrations if you later add Alembic.

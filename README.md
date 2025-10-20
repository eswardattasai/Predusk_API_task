# Me-API Playground
Adds POST/PUT/DELETE for /profile and keeps write-protected CRUD for skills/projects/education/work.

## Run
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend python -c "from app.seed import run; run()"
uvicorn app.main:app --app-dir backend --reload

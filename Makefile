# Dev shortcuts
.PHONY: venv install run ui seed check format

venv:
	python -m venv .venv

install:
	. .venv/bin/activate && pip install -r backend/requirements.txt

run:
	. .venv/bin/activate && uvicorn app.main:app --app-dir backend --reload

ui:
	python -m http.server --directory frontend 5500

seed:
	. .venv/bin/activate && PYTHONPATH=backend python -c "from app.seed import run; run()"

check:
	python -c "import importlib; importlib.import_module('uvicorn'); print('uvicorn ok')"
	python - <<'PY'
from importlib import import_module
import_module('sqlmodel')
print('sqlmodel ok')
PY

format:
	@echo "Add black/ruff and extend this target if needed"

# Architecture

## Components
- **FastAPI service** (`backend/app/main.py`): Exposes CRUD routes and search.
- **SQLModel ORM** (`backend/app/models.py`): Single-writer design with Profile as the root aggregate.
- **Seeder** (`backend/app/seed.py`): Idempotent, can load from dict or JSON.
- **Static UI** (`frontend/index.html`): Minimal fetch() client with Health bar.

## Data Flow
```
[Browser UI] --HTTP--> [FastAPI] --SQLAlchemy/SQLModel--> [DB]
```

## Notable Decisions
- `Project.skills` stored as **JSON array** for simple tag searching via LIKE on SQLite; switch to Postgres JSONB for advanced querying.
- Write endpoints are protected with **HTTP Basic Auth** (simple for demos).
- CORS is wide open for easier hosting across domains.

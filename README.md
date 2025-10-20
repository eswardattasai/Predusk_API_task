# Me‑API Playground — Uma Eswar Datta Sai

![Status](https://img.shields.io/badge/status-live-brightgreen) 
![FastAPI](https://img.shields.io/badge/FastAPI-0.114-009688) 
![SQLModel](https://img.shields.io/badge/SQLModel-0.0.22-4B8) 
![License](https://img.shields.io/badge/license-MIT-blue)

A tiny, production‑ready portfolio API + minimal frontend to showcase **profile, skills, projects, education, and work experience**.  
Built with **FastAPI + SQLModel** (SQLite/Postgres), seeded from your resume, and paired with a static HTML UI.

> Backend: FastAPI (CRUD) • Frontend: Static HTML with fetch() • Health bar • Search by **project skills**

---

## ✨ Features
- **Profile API**: Full CRUD (create/read/update/delete) with Basic Auth for writes
- **Projects & Skills**: Projects include a `skills: string[]` field; search by keyword matches title, description, or `project.skills`
- **Top Skills**: Ranked by `level`
- **Health Bar**: `/api/v1/health` endpoint + visual bar in the UI
- **Seed script**: idempotent seeding from a single Python dict or external JSON
- **Dockerfile**: Portable container build
- **Cloud-ready**: Render (backend) + Vercel (frontend)

---

## 🧱 Architecture (at a glance)
```
repo-root/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app + endpoints
│   │   ├── models.py        # SQLModel tables (Profile, Links, Education, Skill, Project, WorkExperience)
│   │   ├── database.py      # engine, session, init
│   │   ├── auth.py          # Basic auth for writes
│   │   └── seed.py          # DRY, idempotent seeding
│   ├── requirements.txt
│   └── run.sh
├── frontend/
│   └── index.html           # Minimal UI (profile, top skills, search, health bar)
├── docs/
│   ├── ARCHITECTURE.md
│   └── API.md
├── .github/workflows/ci.yml # CI sanity checks
├── .env.example             # Env variables reference
├── Makefile                 # Dev shortcuts
├── Dockerfile               # Backend container
├── vercel.json              # Frontend static config (optional)
└── README.md                # You are here
```

**Data model (simplified):**
```
Profile 1─1 Links
Profile 1─* Education
Profile 1─* Skill
Profile 1─* Project (Project has JSON skills: [string])
Profile 1─* WorkExperience
```

---

## 🚀 Quickstart (Local)

```bash
make venv            # create .venv
make install         # pip install -r backend/requirements.txt
make seed            # run the seeder once
make run             # start FastAPI on http://localhost:8000
make ui              # start static frontend on http://localhost:5500
```

Manual equivalents:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend python -c "from app.seed import run; run()"
uvicorn app.main:app --app-dir backend --reload
python -m http.server --directory frontend 5500
```

---

## 🔌 Configuration
Copy `.env.example` to `.env` and set variables (especially in production):

```env
# backend
DATABASE_URL=sqlite:///./meapi.db  # or postgres://USER:PASS@HOST:5432/DB
WRITE_USER=admin
WRITE_PASS=changeme
```

In Docker/Render/Railway, set the same as service env vars.

---

## 🌐 Deploy

### Backend (Render)
- Start command:  
  ```bash
  uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 10000
  ```
- Env vars: `DATABASE_URL`, `WRITE_USER`, `WRITE_PASS`
- After first deploy: seed data from the Render shell:
  ```bash
  PYTHONPATH=backend python -c "from app.seed import run; run()"
  ```

### Frontend (Vercel)
- Root directory: `frontend`
- Framework preset: “Other”
- Set the **API Base** in `index.html` input to your backend URL.

---

## 📚 API Quick Reference

- `GET /api/v1/health` → `{"status":"ok","...":...}`
- `GET /api/v1/profile` → returns denormalized profile bundle
- `POST /api/v1/profile` (Basic Auth) → create profile
- `PUT /api/v1/profile/{id}` (Basic Auth) → update profile
- `DELETE /api/v1/profile/{id}` (Basic Auth) → delete profile (cleans related rows)
- `GET /api/v1/projects?skill=python` → filter by project skill (checks `Project.skills` JSON)
- `POST /api/v1/projects` / `PUT /api/v1/projects/{id}` / `DELETE /api/v1/projects/{id}` (Basic Auth)
- `GET /api/v1/skills/top?limit=5` → top skills
- `POST /api/v1/skills` / `DELETE /api/v1/skills/{id}` (Basic Auth)
- `GET /api/v1/search?q=keyword` → matches in project title/description/**skills**, plus profile `Skill`, `Education`, `WorkExperience`.

More details in [docs/API.md](docs/API.md).

---

## 🧪 Testing & Development

```bash
make check        # import check + simple startup smoke
make format       # optional: add black/isort/ruff and extend this target
```

> CI runs on every push: installs deps, imports the app, and verifies the seed script can be imported.

---

## 🛠 Troubleshooting

- **Empty UI** → Check API base URL on the page; ensure `health` is green. Seed again if needed.
- **Render “Could not import module main”** → Use `uvicorn app.main:app --app-dir backend ...`
- **SQLite path mismatch** → Use absolute `DATABASE_URL` like `sqlite://///full/path/meapi.db` or switch to Postgres.
- **CORS** → Middleware is open (`*`). If you lock it down, add your frontend domain.

---

## 👤 Author
- **Uma Eswar Datta Sai** (IIT Madras)  
  GitHub: https://github.com/eswardattasai  
  LinkedIn: https://www.linkedin.com/in/k-eswar-datta-sai-371690264/

---

## 📝 License
MIT © 2025-10-20

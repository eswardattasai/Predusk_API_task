# API Reference

Base URL: `http://localhost:8000` (dev) or your Render URL (prod).

## Health
`GET /api/v1/health`

## Profile
- `GET /api/v1/profile`
- `POST /api/v1/profile` (Basic Auth)
- `PUT /api/v1/profile/{id}` (Basic Auth)
- `DELETE /api/v1/profile/{id}` (Basic Auth)

## Projects
- `GET /api/v1/projects?skill=python`
- `POST /api/v1/projects` (Basic Auth)
- `PUT /api/v1/projects/{id}` (Basic Auth)
- `DELETE /api/v1/projects/{id}` (Basic Auth)

## Skills
- `GET /api/v1/skills/top?limit=5`
- `POST /api/v1/skills` (Basic Auth)
- `DELETE /api/v1/skills/{id}` (Basic Auth)

## Search
- `GET /api/v1/search?q=keyword`
  - Matches in `Project.title`, `Project.description`, **`Project.skills`**, and also in profile `Skill`, `Education`, `WorkExperience`.

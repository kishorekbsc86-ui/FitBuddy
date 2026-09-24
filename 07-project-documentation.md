# Project Documentation Phase

## Documentation inventory

| Document | Purpose |
|---|---|
| Root `README.md` | Installation, running, API, test, safety, and deployment notes |
| `.env.example` | Required environment-variable names without secrets |
| `requirements.txt` | Reproducible Python dependencies |
| `project-phases/` | Evidence for all project submission phases |
| FastAPI `/docs` | Interactive API documentation while the app runs |

## API overview

- `GET /health` - health status
- `POST /api/users` - create or refresh a profile and plan
- `GET /api/users` - list saved profiles
- `GET /api/users/{user_id}` - retrieve one profile and plan
- `POST /api/feedback` - revise a plan from feedback

## Configuration

Set `GEMINI_API_KEY` in `.env` for real AI generation. Do not commit `.env`. Hosting providers should store it in their secret environment-variable settings.

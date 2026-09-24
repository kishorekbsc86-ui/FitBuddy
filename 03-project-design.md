# Project Design Phase

## Architecture

```text
Browser / JSON client
        |
FastAPI routes and validation
        |-------------------|
Jinja2 templates       JSON API
        |
AI service --------------------> Google Gemini API
        |
SQLAlchemy ORM ----------------> SQLite database
```

## Main modules

| File or folder | Responsibility |
|---|---|
| `app/main.py` | App creation, static files, startup database setup |
| `app/routes.py` | Web routes, REST endpoints, persistence orchestration |
| `app/schemas.py` | Pydantic validation models |
| `app/database.py` | SQLAlchemy models and SQLite connection |
| `app/services/gemini.py` | Gemini generation and development fallback selection |
| `app/services/fitness.py` | Deterministic offline demo plan and tip generation |
| `templates/` | Input, result, and dashboard pages |
| `static/` | CSS and browser assets |

## Data design

- **User**: external ID, name, age, weight, goal, intensity, creation time.
- **Plan**: original plan, optional revised plan, nutrition tip, optional feedback, update time.
- One user has one current plan record, preserving both original and revised versions.

## UI design

The home page uses a short form. The result page presents the active plan, a tip, and a feedback form. The coach dashboard lists stored profiles with an option to open or delete a plan.

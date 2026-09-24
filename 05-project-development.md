# Project Development Phase

## Implemented features

- FastAPI server with a health endpoint and automatic SQLite table creation.
- HTML forms for creating plans and submitting feedback.
- Gemini plan generation, nutrition/recovery tip generation, and plan revision.
- Safe fallback responses for local development when no Gemini key is set.
- SQLite persistence using SQLAlchemy ORM.
- Coach dashboard listing saved users and plans.
- REST endpoints under `/api/users` and `/api/feedback`.

## How the AI workflow works

1. The route validates form or JSON input.
2. The service creates a goal-specific prompt for Gemini.
3. Gemini returns the workout text or a concise tip.
4. The app stores the response with the user profile.
5. Feedback is combined with the current plan to request a revision.

## Run locally

See the root `README.md` for VS Code setup, dependencies, environment variables, and commands.

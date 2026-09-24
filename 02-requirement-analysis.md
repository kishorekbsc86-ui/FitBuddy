# Requirement Analysis Phase

## Functional requirements

1. Collect a user ID, name, age, weight, goal, and workout intensity.
2. Generate a structured seven-day workout plan.
3. Generate one nutrition or recovery tip.
4. Store profiles, original plans, updated plans, tips, and feedback in SQLite.
5. Allow users to submit feedback and receive a revised plan.
6. Provide a dashboard of saved users and plans.
7. Provide REST API endpoints and FastAPI interactive documentation.

## Non-functional requirements

- Responsive, readable web interface.
- Validation for all incoming profile and feedback data.
- API key stored only in an environment variable, never in source code.
- Local demo works without an API key through a clearly labelled fallback generator.
- Application can run locally with Python and can be deployed as a web service.

## Technology requirements

| Area | Selection |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Templates | Jinja2, HTML, CSS |
| Database | SQLite, SQLAlchemy |
| AI | Google Gemini through `google-genai` |
| Tests | Pytest, FastAPI TestClient |

## Constraints and assumptions

Fitness guidance is educational and is not medical advice. A production deployment should add authentication to the coach dashboard and a managed database instead of local SQLite.

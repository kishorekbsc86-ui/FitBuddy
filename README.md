# FitBuddy - AI Fitness Plan Generator

FitBuddy is a full FastAPI application that creates personalised 7-day fitness plans, saves each profile in SQLite, revises plans from feedback, provides a nutrition/recovery tip, and includes both a browser UI and documented JSON API.

## What is included

- FastAPI backend with Jinja2 pages and `/docs` interactive API documentation
- SQLite + SQLAlchemy storage for users, original plans, updated plans, tips, and feedback
- Gemini integration through the current `google-genai` SDK
- A development fallback so the app still works without an API key (clearly intended for local demos only)
- Responsive home, results, and coach-dashboard pages
- Pytest lifecycle test covering create, feedback update, and retrieval

## VS Code setup (Windows)

1. Open this project folder in VS Code: `File` → `Open Folder` → select the folder containing this README.
2. Open the integrated terminal (`Ctrl+``) and create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` once in that terminal, then activate it again.

3. Install all dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env`. Add your Gemini key to `GEMINI_API_KEY`. Keep the supplied model names or change them to models enabled for your Google account. For a no-key local demo, leave the key blank and leave `ALLOW_DEMO_FALLBACK=true`.

5. Start the app:

   ```powershell
   uvicorn app.main:app --reload
   ```

6. Open `http://127.0.0.1:8000` for FitBuddy and `http://127.0.0.1:8000/docs` for the API explorer.

## Test

Stop the development server if it is running, then run:

```powershell
pytest -q
```

The test uses a temporary local SQLite file and the fallback generator. It does not call Gemini or require a key.

## API examples

- `POST /api/users` creates or refreshes a saved profile and plan.
- `GET /api/users` lists profiles.
- `GET /api/users/{user_id}` retrieves one profile and its plans.
- `POST /api/feedback` revises the current plan.

Example body for `POST /api/users`:

```json
{"user_id":"alex-01","name":"Alex","age":28,"weight_kg":70,"goal":"general wellness","intensity":"medium"}
```

## Safety and privacy notes

Fitness content is general educational guidance, not medical advice. Stop when something hurts and consult a qualified clinician before changing activity when you have injuries, medical conditions, or concerns. The dashboard has no authentication because it is a local demonstration; protect it with authentication and secure database settings before deploying publicly.

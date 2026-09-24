# Project Demonstration Phase

## Local demonstration

1. Start the app with `uvicorn app.main:app`.
2. Open `http://127.0.0.1:8000`.
3. Enter a profile, for example: a goal of general wellness and medium intensity.
4. Select **Generate my 7-day plan**.
5. Submit feedback such as “Add more gentle cardio.”
6. Open **Coach dashboard** to view the saved plan.
7. Visit `http://127.0.0.1:8000/docs` to demonstrate the API.

## Public demonstration

Deploy the repository to Render as a Python Web Service:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variable: `GEMINI_API_KEY` (optional for fallback demo; required for live Gemini)

## Expected outcomes

The demo shows an end-to-end AI application: validated user input, model-generated guidance, database storage, feedback-driven plan revision, and an administrative view.

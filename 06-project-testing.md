# Project Testing Phase

## Automated test

Run from the project root:

```powershell
pytest -q
```

## Test coverage

The lifecycle test verifies:

1. Health endpoint returns success.
2. A valid profile can create a saved plan.
3. A generated plan contains a seven-day structure.
4. Feedback generates and saves a revised plan.
5. The saved profile can be retrieved through the API.

## Manual test checklist

- Submit the home form with each goal and intensity.
- Confirm the result page contains a plan and tip.
- Submit feedback and confirm the revised plan appears.
- Open `/view-all-users` and verify saved profiles.
- Open `/docs` and try API endpoints.
- Confirm `.env` is not displayed by `git status` before any push.

## Latest result

The automated lifecycle test passed locally using the safe no-key fallback mode.

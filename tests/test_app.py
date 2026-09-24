import os
from pathlib import Path
os.environ["DATABASE_URL"] = "sqlite:///./test_fitbuddy.db"
os.environ["ALLOW_DEMO_FALLBACK"] = "true"

from fastapi.testclient import TestClient
from app.database import engine
from app.main import app

def test_health_and_plan_lifecycle():
    database = Path("test_fitbuddy.db")
    if database.exists():
        engine.dispose()
        database.unlink()
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        profile = {"user_id":"test-user", "name":"Taylor", "age":30, "weight_kg":72, "goal":"general wellness", "intensity":"medium"}
        created = client.post("/api/users", json=profile)
        assert created.status_code == 201
        assert "Day 1" in created.json()["original_plan"]
        updated = client.post("/api/feedback", json={"user_id":"test-user", "feedback":"Please add more gentle cardio."})
        assert updated.status_code == 200
        assert "gentle cardio" in updated.json()["updated_plan"]
        assert client.get("/api/users/test-user").status_code == 200
    engine.dispose()
    if database.exists(): database.unlink()

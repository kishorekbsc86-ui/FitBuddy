from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'fitbuddy.db'}")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-2.5-pro")
TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-2.5-flash")
ALLOW_DEMO_FALLBACK = os.getenv("ALLOW_DEMO_FALLBACK", "true").lower() in {"1", "true", "yes"}

import logging
from app.config import ALLOW_DEMO_FALLBACK, GEMINI_API_KEY, TIP_MODEL, WORKOUT_MODEL
from app.schemas import UserInput
from .fitness import demo_plan, demo_tip

logger = logging.getLogger(__name__)

def _generate(prompt: str, model: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model=model, contents=prompt)
    if not response.text:
        raise RuntimeError("Gemini returned no text")
    return response.text.strip()

def generate_workout(profile: UserInput) -> str:
    prompt = f"""You are FitBuddy, a careful fitness coach. Create a clear 7-day workout plan for {profile.name}, age {profile.age}, weight {profile.weight_kg} kg, goal {profile.goal}, intensity {profile.intensity}. Use headings Day 1 through Day 7. Every day needs a warm-up, main workout with exercises/sets/reps or time, and cooldown/recovery. Include two recovery/rest days when appropriate. Keep it beginner-safe, avoid medical claims, and end with a concise safety note. Plain text only."""
    try:
        return _generate(prompt, WORKOUT_MODEL)
    except Exception as exc:
        if not ALLOW_DEMO_FALLBACK: raise
        logger.warning("Gemini plan generation unavailable; using demo fallback: %s", exc)
        return demo_plan(profile)

def generate_tip(profile: UserInput) -> str:
    prompt = f"Give one concise, practical nutrition or recovery tip for a person pursuing {profile.goal} at {profile.intensity} workout intensity. Avoid medical claims."
    try:
        return _generate(prompt, TIP_MODEL)
    except Exception as exc:
        if not ALLOW_DEMO_FALLBACK: raise
        logger.warning("Gemini tip generation unavailable; using demo fallback: %s", exc)
        return demo_tip(profile.goal)

def revise_plan(profile: UserInput, original_plan: str, feedback: str) -> str:
    prompt = f"""Revise this 7-day fitness plan for {profile.name} (goal: {profile.goal}; intensity: {profile.intensity}) based on this feedback: {feedback!r}. Preserve a clear Day 1 to Day 7 structure with warm-up, main work and cooldown. Keep it safe and practical.\n\nCURRENT PLAN:\n{original_plan}"""
    try:
        return _generate(prompt, WORKOUT_MODEL)
    except Exception as exc:
        if not ALLOW_DEMO_FALLBACK: raise
        logger.warning("Gemini revision unavailable; using demo fallback: %s", exc)
        return demo_plan(profile, feedback)

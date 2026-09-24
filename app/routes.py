from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from .config import BASE_DIR
from .database import Plan, User, get_db
from .schemas import FeedbackInput, UserInput
from .services.gemini import generate_tip, generate_workout, revise_plan

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def _profile(user: User) -> UserInput:
    return UserInput(user_id=user.external_id, name=user.name, age=user.age, weight_kg=user.weight_kg, goal=user.goal, intensity=user.intensity)

def _load_user(db: Session, external_id: str) -> User:
    user = db.query(User).options(joinedload(User.plan)).filter(User.external_id == external_id).first()
    if not user: raise HTTPException(status_code=404, detail="User ID not found")
    return user

def _upsert_plan(db: Session, profile: UserInput) -> User:
    user = db.query(User).filter(User.external_id == profile.user_id).first()
    plan_text, tip = generate_workout(profile), generate_tip(profile)
    if user:
        user.name, user.age, user.weight_kg, user.goal, user.intensity = profile.name, profile.age, profile.weight_kg, profile.goal, profile.intensity
        if user.plan:
            user.plan.original_plan, user.plan.updated_plan, user.plan.feedback, user.plan.nutrition_tip = plan_text, None, None, tip
        else: user.plan = Plan(original_plan=plan_text, nutrition_tip=tip)
    else:
        user = User(external_id=profile.user_id, name=profile.name, age=profile.age, weight_kg=profile.weight_kg, goal=profile.goal, intensity=profile.intensity, plan=Plan(original_plan=plan_text, nutrition_tip=tip))
        db.add(user)
    db.commit(); db.refresh(user)
    return user

def _result_context(request: Request, user: User, message: str | None = None):
    return {"request": request, "user": user, "plan": user.plan, "active_plan": user.plan.updated_plan or user.plan.original_plan, "message": message}

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@router.post("/generate-workout")
def generate_from_form(request: Request, user_id: str = Form(), name: str = Form(), age: int = Form(), weight_kg: float = Form(), goal: str = Form(), intensity: str = Form(), db: Session = Depends(get_db)):
    try: profile = UserInput(user_id=user_id, name=name, age=age, weight_kg=weight_kg, goal=goal, intensity=intensity)
    except Exception as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    user = _upsert_plan(db, profile)
    return templates.TemplateResponse(request, "result.html", _result_context(request, user, "Your 7-day plan is ready."))

@router.get("/users/{user_id}")
def user_result(request: Request, user_id: str, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request, "result.html", _result_context(request, _load_user(db, user_id)))

@router.post("/submit-feedback")
def feedback_from_form(request: Request, user_id: str = Form(), feedback: str = Form(), db: Session = Depends(get_db)):
    payload = FeedbackInput(user_id=user_id, feedback=feedback)
    user = _load_user(db, payload.user_id)
    user.plan.updated_plan = revise_plan(_profile(user), user.plan.updated_plan or user.plan.original_plan, payload.feedback)
    user.plan.feedback = payload.feedback
    user.plan.nutrition_tip = generate_tip(_profile(user))
    db.commit(); db.refresh(user)
    return templates.TemplateResponse(request, "result.html", _result_context(request, user, "Plan updated from your feedback."))

@router.get("/view-all-users")
def all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).options(joinedload(User.plan)).order_by(User.created_at.desc()).all()
    return templates.TemplateResponse(request, "all_users.html", {"users": users})

@router.post("/users/{user_id}/delete")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = _load_user(db, user_id); db.delete(user); db.commit()
    return RedirectResponse("/view-all-users", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/api/users", status_code=status.HTTP_201_CREATED)
def api_create_user(profile: UserInput, db: Session = Depends(get_db)):
    user = _upsert_plan(db, profile)
    return serialize(user)

@router.get("/api/users")
def api_list_users(db: Session = Depends(get_db)):
    return [serialize(user) for user in db.query(User).options(joinedload(User.plan)).all()]

@router.get("/api/users/{user_id}")
def api_get_user(user_id: str, db: Session = Depends(get_db)):
    return serialize(_load_user(db, user_id))

@router.post("/api/feedback")
def api_feedback(payload: FeedbackInput, db: Session = Depends(get_db)):
    user = _load_user(db, payload.user_id)
    user.plan.updated_plan = revise_plan(_profile(user), user.plan.updated_plan or user.plan.original_plan, payload.feedback)
    user.plan.feedback, user.plan.nutrition_tip = payload.feedback, generate_tip(_profile(user))
    db.commit(); db.refresh(user)
    return serialize(user)

def serialize(user: User) -> dict:
    return {"user_id": user.external_id, "name": user.name, "age": user.age, "weight_kg": user.weight_kg, "goal": user.goal, "intensity": user.intensity, "original_plan": user.plan.original_plan, "updated_plan": user.plan.updated_plan, "nutrition_tip": user.plan.nutrition_tip, "feedback": user.plan.feedback}

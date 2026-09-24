from app.schemas import UserInput

def demo_plan(profile: UserInput, feedback: str | None = None) -> str:
    volume = {"low": "2 sets, relaxed pace", "medium": "3 sets, steady pace", "high": "4 sets, challenging but controlled"}[profile.intensity]
    focus = {"weight loss": "full-body strength and low-impact cardio", "muscle gain": "progressive resistance training", "general wellness": "balanced movement and mobility", "flexibility": "mobility and controlled stretching", "endurance": "aerobic base and muscular endurance"}[profile.goal]
    adjustment = f"\nPlan adjustment: {feedback.strip()}" if feedback else ""
    days = [("Day 1", f"{focus.title()} - squat pattern, push movement, 20-minute walk"), ("Day 2", "Mobility - gentle yoga, hip and shoulder mobility"), ("Day 3", "Cardio - brisk walk, cycle, or swim at conversational pace"), ("Day 4", "Strength - hinge pattern, row movement, core stability"), ("Day 5", "Recovery - easy walk and full-body stretching"), ("Day 6", "Choice session - repeat the week’s most enjoyable workout"), ("Day 7", "Rest - sleep, hydration, and a relaxed walk if desired")]
    lines = [f"7-Day {profile.goal.title()} Plan ({profile.intensity.title()} intensity)", "Safety: stop for pain, choose loads you can control, and seek clinical advice for medical concerns.", ""]
    for day, workout in days:
        lines.extend([day, "Warm-up: 5-10 minutes of easy movement.", f"Main: {workout} ({volume}).", "Cooldown: 5 minutes easy breathing and stretching.", ""])
    return "\n".join(lines) + adjustment

def demo_tip(goal: str) -> str:
    tips = {"weight loss": "Build meals around vegetables, fibre-rich carbohydrates, and a protein source so you stay satisfied.", "muscle gain": "Include a protein-rich food after training and spread protein across regular meals.", "general wellness": "Keep a water bottle nearby and aim for colourful plants plus a protein source at most meals.", "flexibility": "Hydrate throughout the day and include regular meals to support recovery from mobility work.", "endurance": "Eat a carbohydrate-containing snack before longer sessions and replace fluids afterwards."}
    return tips[goal]

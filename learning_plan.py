
from ai_service import generate_learning_plan


def create_plan(subject, goal, level, duration_days, daily_minutes):
    """Generate a learning plan using Gemini AI."""

    if not subject.strip():
        return "Please enter a subject."

    if not goal.strip():
        return "Please enter a learning goal."

    if duration_days < 1:
        return "Duration must be at least 1 day."

    if daily_minutes < 1:
        return "Daily study time must be at least 1 minute."

    plan = generate_learning_plan(
        subject,
        goal,
        level,
        duration_days,
        daily_minutes
    )

    return plan

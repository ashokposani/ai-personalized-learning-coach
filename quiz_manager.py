
from ai_service import generate_quiz


def create_quiz(topic, level, number_of_questions=5):
    """Generate quiz questions for a topic."""
    return generate_quiz(topic, level, number_of_questions)


def score_quiz(questions, user_answers):
    """Calculate the quiz score using Python."""

    if isinstance(questions, dict) and "error" in questions:
        return {
            "score": 0,
            "total": 0,
            "percentage": 0,
            "message": questions["error"]
        }

    total = len(questions)
    score = 0
    results = []

    for index, question in enumerate(questions):
        selected = user_answers.get(str(index))

        try:
            selected = int(selected)
        except (TypeError, ValueError):
            selected = -1

        correct = selected == question["answer"]

        if correct:
            score += 1

        results.append({
            "question": question["question"],
            "selected_answer": selected,
            "correct_answer": question["answer"],
            "is_correct": correct,
            "explanation": question["explanation"]
        })

    percentage = round((score / total) * 100) if total else 0

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "results": results
    }

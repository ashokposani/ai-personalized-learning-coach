
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def ask_gemini(prompt):
    if client is None:
        return "Error: Gemini API key not found. Please check your .env file."

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Gemini API Error: {e}"


def generate_learning_plan(subject, goal, level, duration_days, daily_minutes):
    prompt = f"""
    Create a personalized learning plan.
    Subject: {subject}
    Learning goal: {goal}
    Current level: {level}
    Duration: {duration_days} days
    Daily study time: {daily_minutes} minutes

    Return a clear plan organized by day, with topics,
    learning activities, and a small task for each day.
    Use simple language.
    """

    return ask_gemini(prompt)


def generate_quiz(topic, level, number_of_questions=5):
    prompt = f"""
    Create {number_of_questions} multiple-choice quiz questions
    about: {topic}
    Difficulty level: {level}

    Return ONLY a valid JSON array. Each item must contain:
    "question": question text,
    "options": exactly four answer choices,
    "answer": the zero-based index of the correct option (0-3),
    "explanation": a short explanation.

    Do not include Markdown code fences.
    """

    result = ask_gemini(prompt)

    try:
        start = result.find("[")
        end = result.rfind("]") + 1
        if start == -1 or end == 0:
            raise ValueError("JSON array not found")

        questions = json.loads(result[start:end])

        if not isinstance(questions, list) or not questions:
            raise ValueError("Empty quiz")

        for q in questions:
            if (
                not isinstance(q.get("question"), str)
                or not isinstance(q.get("options"), list)
                or len(q["options"]) != 4
                or not isinstance(q.get("answer"), int)
                or q["answer"] not in range(4)
                or not isinstance(q.get("explanation"), str)
            ):
                raise ValueError("Invalid quiz format")

        return questions

    except (ValueError, json.JSONDecodeError, AttributeError):
        return {
            "error": "Could not create a valid quiz. Please try again.",
            "details": result
        }


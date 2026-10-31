
from pathlib import Path

project = Path(__file__).parent

files = {
    "app.py": "",
    "ai_service.py": "",
    "learning_plan.py": "",
    "quiz_manager.py": "",
    "database.py": "",
    "requirements.txt": """streamlit
google-genai
python-dotenv
""",
    ".env.example": "GEMINI_API_KEY=your_api_key_here\n",
    ".gitignore": """.env
__pycache__/
*.pyc
learning_coach.db
.venv/
""",
    "README.md": """# AI Personalized Learning Coach

An AI-powered learning application built with
Python, Streamlit, Gemini API, and SQLite.

## Features
- Personalized study plans
- Topic-based practice quizzes
- Automatic quiz scoring
- Weak-topic recommendations
- Learning progress dashboard
- SQLite progress storage

## Run
1. Install dependencies:
   pip install -r requirements.txt

2. Configure your Gemini API key in .env

3. Start the application:
   streamlit run app.py
""",
    "sample_data/example_learning_plan.json": """{
  "subject": "Python",
  "goal": "Learn Python fundamentals",
  "level": "Beginner",
  "duration_days": 7,
  "daily_minutes": 45,
  "topics": []
}
"""
}

for name, content in files.items():
    path = project / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

print("Project structure created successfully!")
print(f"Project location: {project}")
print("Next: install the required packages.")

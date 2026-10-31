
import streamlit as st
from learning_plan import create_plan
from quiz_manager import create_quiz, score_quiz
from database import init_db

st.set_page_config(
    page_title="AI Personalized Learning Coach",
    page_icon="📚",
    layout="wide"
)

init_db()

st.title("📚 AI Personalized Learning Coach")
st.write("Your personal AI tutor for study plans, quizzes, and progress.")

tab1, tab2 = st.tabs(["🎯 Study Plan", "📝 Quiz"])

with tab1:
    st.header("Create Your Learning Plan")

    with st.form("plan_form"):
        subject = st.text_input("What do you want to learn?", "Python")
        goal = st.text_input("Your learning goal", "Learn Python basics")
        level = st.selectbox(
            "Your current level",
            ["Beginner", "Intermediate", "Advanced"]
        )
        duration = st.number_input(
            "Study duration (days)",
            min_value=1,
            max_value=365,
            value=7
        )
        daily_minutes = st.number_input(
            "Daily study time (minutes)",
            min_value=5,
            max_value=600,
            value=30
        )

        create_button = st.form_submit_button("Generate Study Plan")

    if create_button:
        with st.spinner("Creating your personalized plan..."):
            plan = create_plan(
                subject, goal, level, int(duration), int(daily_minutes)
            )

        st.session_state["learning_plan"] = plan
        st.subheader("Your Study Plan")
        st.markdown(plan)

with tab2:
    st.header("Practice Quiz")

    topic = st.text_input("Quiz topic", "Python variables")
    quiz_level = st.selectbox(
        "Quiz difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        key="quiz_level"
    )

    if st.button("Generate Quiz"):
        with st.spinner("Creating quiz questions..."):
            questions = create_quiz(topic, quiz_level)

        if isinstance(questions, dict) and "error" in questions:
            st.error(questions["error"])
            st.text(str(questions.get("details", "")))
        elif isinstance(questions, list) and questions:
            st.session_state["quiz_questions"] = questions
            st.session_state["quiz_topic"] = topic
            st.session_state.pop("quiz_result", None)

    questions = st.session_state.get("quiz_questions", [])

    if questions:
        with st.form("quiz_form"):
            answers = {}

            for i, question in enumerate(questions):
                st.write(f"**{i + 1}. {question['question']}**")
                options = question["options"]

                answers[str(i)] = st.radio(
                    "Choose your answer:",
                    options=list(range(len(options))),
                    format_func=lambda x, opts=options: opts[x],
                    key=f"answer_{i}"
                )

            submitted = st.form_submit_button("Check My Score")

        if submitted:
            result = score_quiz(questions, answers)
            st.session_state["quiz_result"] = result

        result = st.session_state.get("quiz_result")

        if result:
            st.subheader("Your Quiz Result")
            st.metric(
                "Score",
                f"{result['score']} / {result['total']}"
            )
            st.progress(result["percentage"] / 100)
            st.write(f"Percentage: {result['percentage']}%")

            for item in result.get("results", []):
                if item["is_correct"]:
                    st.success("Correct: " + item["question"])
                else:
                    st.error("Incorrect: " + item["question"])

                st.write(
                    "Correct answer: "
                    + questions[result["results"].index(item)]["options"][
                        item["correct_answer"]
                    ]
                )
                st.write("Explanation: " + item["explanation"])

st.divider()
st.caption("Learning Coach | Python • Streamlit • Gemini AI • SQLite")

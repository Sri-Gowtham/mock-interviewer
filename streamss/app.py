import streamlit as st
from crewai import Agent, Task, Crew

# ==============================
# STREAMLIT UI
# ==============================
st.title("🤖 AI Mock Interviewer (CrewAI)")

role = st.selectbox("Select Job Role", [
    "Data Scientist",
    "Web Developer",
    "UI/UX Designer"
])

# ==============================
# AGENTS
# ==============================

question_agent = Agent(
    role="Question Generator",
    goal=f"Ask interview questions for a {role}",
    backstory="Expert interviewer who asks role-specific questions"
)

feedback_agent = Agent(
    role="Feedback Generator",
    goal="Give short feedback on answers",
    backstory="Provides constructive feedback to improve answers"
)

# ==============================
# QUESTIONS (dynamic per role)
# ==============================

questions_db = {
    "Data Scientist": [
        "What is overfitting?",
        "Explain bias vs variance.",
        "What is cross-validation?",
        "Difference between regression and classification?",
        "What is a confusion matrix?"
    ],
    "Web Developer": [
        "What is REST API?",
        "Difference between GET and POST?",
        "What is responsive design?",
        "Explain JavaScript closures.",
        "What is DOM?"
    ],
    "UI/UX Designer": [
        "What is user-centered design?",
        "Difference between UI and UX?",
        "What is wireframing?",
        "Explain usability testing.",
        "What is a design system?"
    ]
}

# ==============================
# SESSION STATE
# ==============================

if "index" not in st.session_state:
    st.session_state.index = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

questions = questions_db[role]

# ==============================
# INTERVIEW FLOW
# ==============================

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.subheader(f"Q{st.session_state.index+1}: {q}")

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        # TASK 1: Analyze Answer
        analysis_task = Task(
            description=f"Analyze this answer: {answer}",
            agent=feedback_agent
        )

        # TASK 2: Give Feedback
        feedback_task = Task(
            description=f"Give short feedback for this answer: {answer}",
            agent=feedback_agent
        )

        crew = Crew(
            agents=[feedback_agent],
            tasks=[analysis_task, feedback_task],
            process="sequential"
        )

        result = crew.kickoff()

        st.success("✅ Feedback:")
        st.write(result)

        st.session_state.answers.append(answer)
        st.session_state.index += 1

else:
    st.success("🎉 Interview Completed!")
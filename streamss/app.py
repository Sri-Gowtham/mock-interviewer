import streamlit as st
import os
import google.generativeai as genai
from crewai import Agent, Task, Crew

# ==============================
# SET GEMINI API KEY
# ==============================
GEMINI_API_KEY = os.getenv("AIzaSyCX_4EkRh2325PiOUzy2O23hQfj6-4rjsA")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

# ==============================
# STREAMLIT UI
# ==============================
st.title("🤖 AI Mock Interviewer (CrewAI + Gemini)")

role = st.selectbox("Select Role", [
    "Data Scientist",
    "Web Developer",
    "UI/UX Designer"
])

# ==============================
# CREWAI AGENTS
# ==============================

question_agent = Agent(
    role="Question Generator",
    goal=f"Generate interview questions for {role}",
    backstory="Expert interviewer who asks role-specific questions"
)

feedback_agent = Agent(
    role="Feedback Agent",
    goal="Provide short and helpful feedback",
    backstory="Helps candidates improve their answers"
)

# ==============================
# QUESTIONS DATABASE
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

questions = questions_db[role]

# ==============================
# INTERVIEW FLOW
# ==============================

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.subheader(f"Q{st.session_state.index+1}: {q}")

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):

        try:
            # CrewAI Task
            task = Task(
                description=f"Give short feedback for this answer: {answer}",
                agent=feedback_agent
            )

            crew = Crew(
                agents=[feedback_agent],
                tasks=[task],
                process="sequential"
            )

            crew_result = crew.kickoff()

            # Gemini API Feedback
            response = model.generate_content(
                f"Give short interview feedback for this answer:\n{answer}"
            )

            st.success("🤖 AI Feedback:")
            st.write(response.text)

        except Exception as e:
            # Fallback (important for safety)
            st.warning("⚠ API not working → showing fallback")

            if len(answer) > 50:
                st.success("✅ Good explanation!")
            elif len(answer) > 20:
                st.info("👍 Try to add more details.")
            else:
                st.error("❌ Answer too short.")

        st.session_state.index += 1

else:
    st.success("🎉 Interview Completed!")
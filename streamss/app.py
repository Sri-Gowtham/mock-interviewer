import streamlit as st
from crewai import Agent, Task, Crew

st.title("🤖 AI Mock Interviewer (CrewAI)")

role = st.selectbox("Select Job Role", [
    "Data Scientist",
    "Web Developer",
    "UI/UX Designer"
])

# Agents
question_agent = Agent(
    role="Question Generator",
    goal=f"Ask interview questions for a {role}",
    backstory="Expert interviewer"
)

feedback_agent = Agent(
    role="Feedback Generator",
    goal="Give feedback",
    backstory="Gives short feedback"
)

questions_db = {
    "Data Scientist": [
        "What is overfitting?",
        "Explain bias vs variance.",
        "What is cross-validation?",
        "Regression vs classification?",
        "What is confusion matrix?"
    ],
    "Web Developer": [
        "What is REST API?",
        "GET vs POST?",
        "Responsive design?",
        "JS closures?",
        "What is DOM?"
    ],
    "UI/UX Designer": [
        "User-centered design?",
        "UI vs UX?",
        "Wireframing?",
        "Usability testing?",
        "Design system?"
    ]
}

if "index" not in st.session_state:
    st.session_state.index = 0

questions = questions_db[role]

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.subheader(f"Q{st.session_state.index+1}: {q}")

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        try:
            # CrewAI execution (if API available)
            task = Task(
                description=f"Give short feedback for this answer: {answer}",
                agent=feedback_agent
            )

            crew = Crew(
                agents=[feedback_agent],
                tasks=[task],
                process="sequential"
            )

            result = crew.kickoff()
            st.success(result)

        except:
            # ✅ FALLBACK (IMPORTANT)
            st.warning("⚠ API not available → Showing fallback feedback")

            if len(answer) > 50:
                st.success("✅ Good explanation!")
            elif len(answer) > 20:
                st.info("👍 Try adding more detail.")
            else:
                st.error("❌ Answer too short.")

        st.session_state.index += 1

else:
    st.success("🎉 Interview Completed!")
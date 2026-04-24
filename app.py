import streamlit as st
import os
import google.generativeai as genai

# ==============================
# LOAD API KEY FROM STREAMLIT SECRETS
# ==============================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None)
if not GEMINI_API_KEY:
    st.error("⚠️ API Key not found. Please add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

# ==============================
# STREAMLIT UI
# ==============================
st.title("🤖 AI Mock Interviewer")

role = st.selectbox("Select Role", [
    "Data Scientist",
    "Web Developer",
    "UI/UX Designer"
])

# ==============================
# QUESTIONS DATABASE
# ==============================
questions_db = {
    "Data Scientist": [
        "What is overfitting in machine learning?",
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
# SIMPLE FEEDBACK FUNCTION
# ==============================
def get_feedback(answer):
    if len(answer) > 50:
        return "✅ Good explanation!"
    elif len(answer) > 20:
        return "👍 Try to add more details."
    else:
        return "❌ Answer too short."

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
    st.subheader(f"Q{st.session_state.index + 1}: {q}")

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):
        try:
            # Gemini API Feedback
            response = model.generate_content(
                f"Give short interview feedback for this answer:\n{answer}"
            )

            st.success("🤖 AI Feedback:")
            st.write(response.text)

        except:
            # Fallback feedback
            st.warning("⚠ API issue → showing basic feedback")
            feedback = get_feedback(answer)
            st.write(feedback)

        st.session_state.index += 1
        st.rerun()

else:
    st.success("🎉 Interview Completed!")
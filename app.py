import streamlit as st
import json

from prompts.prompt_builder import build_prompt
from services.llm_service import get_ai_response
from utils.response_formatter import format_response
from utils.data_pipeline import log_interaction
from config.settings import Settings


# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="EduLocal AI", layout="wide")

# ---------------------------
# SESSION STATE (CHAT MEMORY)
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("🎓 EduLocal AI")

mode = st.sidebar.selectbox(
    "Learning Mode",
    ["Learn", "Exam Prep", "Quick Answer"]
)

language = st.sidebar.selectbox(
    "Language",
    Settings.SUPPORTED_LANGUAGES
)

st.sidebar.markdown("### 🕘 Recent Questions")

try:
    with open("data/logs.json", "r") as f:
        logs = json.load(f)[-5:]
        for item in reversed(logs):
            st.sidebar.write(f"- {item['question']}")
except:
    st.sidebar.write("No history yet.")

# ---------------------------
# BANNER
# ---------------------------
st.image("assets/banner.png", use_column_width=True)

# ---------------------------
# CHAT DISPLAY
# ---------------------------
for msg in st.session_state.messages:

    content = msg["content"].replace("\n", "<br>")

    if msg["role"] == "user":

        user_html = f"""
        <div style="text-align:right; margin-bottom:10px;">
            <div style="
                display:inline-block;
                background:#3b3b3b;
                padding:12px 16px;
                border-radius:15px;
                color:white;
                max-width:70%;
                word-wrap:break-word;
            ">
                {content}
            </div>
        </div>
        """

        st.markdown(user_html, unsafe_allow_html=True)

    else:

        ai_html = f"""
        <div style="text-align:left; margin-bottom:10px;">
            <div style="
                display:inline-block;
                background:#1e1e1e;
                padding:14px 18px;
                border-radius:15px;
                color:white;
                max-width:70%;
                border:1px solid #2c2c2c;
                word-wrap:break-word;
            ">
                {content}
            </div>
        </div>
        """

        st.markdown(ai_html, unsafe_allow_html=True)
# ---------------------------
# USER INPUT
# ---------------------------
question = st.text_input("💬 Ask a question")

# ---------------------------
# MODE → DIFFICULTY
# ---------------------------
if mode == "Learn":
    difficulty = "simple"
elif mode == "Exam Prep":
    difficulty = "exam-level"
else:
    difficulty = "concise"

# ---------------------------
# SEND BUTTON
# ---------------------------
if st.button("Send"):

    if question.strip():

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.spinner("🧠 Thinking..."):

            messages = build_prompt(
                question,
                language,
                difficulty,
                chat_history=st.session_state.messages
            )
            raw = get_ai_response(messages)
            formatted = format_response(raw)

            ai_response = f"""
<b>📘 Explanation:</b><br>{formatted["explanation"]}<br><br>
<b>📍 Example:</b><br>{formatted["example"]}
"""

            # Add AI message
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response
            })

            # Log
            log_interaction(question, raw, language, difficulty)

        st.rerun()

# ---------------------------
# FOLLOW-UP BUTTONS
# ---------------------------
st.markdown("### 🔁 Continue Learning")

col1, col2, col3 = st.columns(3)

follow_q = None

if col1.button("Explain Simpler"):
    follow_q = f"Explain this more simply: {question}"

elif col2.button("Another Example"):
    follow_q = f"Give another example for: {question}"

elif col3.button("Test Me"):
    follow_q = f"Create a quiz question on: {question}"


if follow_q:

    st.session_state.messages.append({
        "role": "user",
        "content": follow_q
    })

    with st.spinner("🧠 Thinking..."):

        messages = build_prompt(
            follow_q,
            language,
            difficulty,
            chat_history=st.session_state.messages
        )
        raw = get_ai_response(messages)
        formatted = format_response(raw)

        ai_response = f"""
<b>📘 Explanation:</b><br>{formatted["explanation"]}<br><br>
<b>📍 Example:</b><br>{formatted["example"]}
"""

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })

    st.rerun()
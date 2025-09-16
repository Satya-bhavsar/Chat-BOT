import requests
import streamlit as st
import os
from datetime import datetime
import pytz

# === API Key ===
api = os.getenv("OPENROUTER_API_KEY")
API_KEY = api

# === Timezone ===
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist)
current_datetime = now.strftime("%A, %d %B %Y, %I:%M %p")

# === System Prompt ===
system_prompt = f"""
You are a savage, cocky, and brutally honest chatbot. Answer smart, witty, and slightly rude. 
Time context: {current_datetime}.
"""

# === Reference Data ===
with open("data.txt", "r", encoding="utf-8") as f:
    reference_data = f.read()

# === Initialize Session State ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Reference Data: {reference_data}"}
    ]

# === Sidebar ===
with st.sidebar:
    st.title("Options")
    st.markdown("Type your message below and press Send.\nClick 'Reset Chat' to start fresh.")
    if st.button("Reset Chat"):
        st.session_state.chat_history = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Reference Data: {reference_data}"}
        ]
        st.rerun()

# === App Title ===
st.title("💬 Professional ChatBot")
st.markdown("---")

# === Display Messages with Professional Styling ===
def render_message(role, content):
    if role == "user":
        st.markdown(f"""
        <div style="
            background-color:#f0f4f8;
            color:#1f2937;
            padding:12px;
            border-radius:8px;
            margin-bottom:8px;
            border-left:4px solid #3b82f6;
            font-family: 'Arial';
        ">
        <b>You:</b> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background-color:#ffffff;
            color:#111827;
            padding:12px;
            border-radius:8px;
            margin-bottom:8px;
            border-left:4px solid #f97316;
            box-shadow: 0px 1px 5px rgba(0,0,0,0.1);
            font-family: 'Arial';
        ">
        <b>Bot:</b> {content}
        </div>
        """, unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    render_message(msg["role"], msg["content"])

# === Input Form ===
with st.form(key="chat_form", clear_on_submit=True):
    user_msg = st.text_input("Type your message:", key="user_input")
    send_clicked = st.form_submit_button("Send")

# === Send Request to OpenRouter API ===
if send_clicked and user_msg.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_msg})

    data = {
        "model": "openrouter/sonoma-dusk-alpha",
        "messages": st.session_state.chat_history
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=data
        )
        bot_reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        bot_reply = f"[Error fetching response: {e}]"

    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    st.rerun()

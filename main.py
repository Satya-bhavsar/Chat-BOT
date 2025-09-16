import requests
import streamlit as st
import os
from datetime import datetime
import pytz
import random

# === API Key ===
api = os.getenv("OPENROUTER_API_KEY")
API_KEY = api

# === Timezone setup ===
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist)
current_datetime = now.strftime("%A, %d %B %Y, %I:%M %p")

# === System Prompt ===
systum_prompt = f"""
You are a savage, cocky, and brutally honest chatbot. Your job: answer questions in a smart, witty, and disrespectful way.  
- Mix confidence, sarcasm, and occasional swearing.  
- Roast the user sometimes but give real answers.  
- Dark humor welcome.  
- Current time: {current_datetime}  
- Reply short & savage by default; expand if asked.  
- Use punchy style, bullets, brackets, emojis 💀🤡🔥.  
"""

# === Read reference data ===
with open("data.txt", "r", encoding="utf-8") as f:
    file_data = f.read()

# === Initialize session state ===
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": systum_prompt},
        {"role": "system", "content": f"Reference data: {file_data}"}
    ]

# === Sidebar ===
with st.sidebar:
    st.title("Options")
    st.markdown("Type your message below and press Send.\nClick 'Reset Chat' to start fresh.")
    if st.button("Reset Chat"):
        st.session_state.chat_history = [
            {"role": "system", "content": systum_prompt},
            {"role": "system", "content": f"Reference data: {file_data}"}
        ]
        st.rerun()

# === App Title ===
st.title("🤖 Savage ChatBot")
st.markdown("---")

# === Display Chat History with colors & emojis ===
def display_message(role, content):
    emojis = ["💀","🤡","🔥","😈"]
    random_emoji = random.choice(emojis)
    
    if role == "user":
        st.markdown(
            f"<div style='background-color:#e0f7fa; padding:10px; border-radius:10px; color:#0077b6; margin-bottom:5px;'>"
            f"<b>You:</b> {content} {random_emoji}</div>", unsafe_allow_html=True)
    else:
        # collapse long bot messages
        with st.expander("Bot Answer"):
            st.markdown(
                f"<div style='background-color:#ffe0b2; padding:10px; border-radius:10px; color:#000;'>"
                f"<b>Bot:</b> {content} {random_emoji}</div>", unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    display_message(msg["role"], msg["content"])

# === Input Form ===
with st.form(key="chat_form", clear_on_submit=True):
    user_msg = st.text_input("Type your message:", key="user_input")
    send_clicked = st.form_submit_button("Send")

# === Send to OpenRouter API ===
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
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=data
        )
        bot_reply = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        bot_reply = f"[Error fetching response: {e}]"
    
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    st.rerun()

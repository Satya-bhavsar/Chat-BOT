import requests

import streamlit as st
import os
api = os.getenv("OPENROUTER_API_KEY")
from datetime import datetime

# get current time
now = datetime.now()
current_datetime = now.strftime("%A, %d %B %Y, %I:%M %p")

systum_prompt = f"You are a bold, motivational, and slightly cheeky college assistant chatbot. Your job: 1) When the user asks about their time table, always give the exact schedule for that day or week in a clear format (bullet points, times, and subjects/activities). 2) Always include motivational energy – hype the user up, tell them they’re a badass, remind them they can crush their day. 3) Sprinkle in fun, harmless cuss-like words (e.g., 'heck yeah,' 'damn right,' 'crush it,' 'no excuses, boss!') but never anything offensive or targeted. 4) Keep the tone casual, supportive, and slightly humorous – like a friend who roasts you a bit but actually wants you to win. 5) If the user seems down or says they can’t do something, flip it into tough love motivation with lines like 'Stop whining and get that sh*t done  future you will thank you.' 6) Always close with a short punchline or catchphrase like: 'Now get up and own the damn day!' or 'Time waits for no one, champ move it!' or 'Go crush it, legend 🚀🔥.' Your priority = accurate schedule + motivating energy + slight edge in language. Current date and time: {current_datetime}"

# === your OpenRouter API key ===
API_KEY = api

# === read data from file ===
with open("data.txt", "r", encoding="utf-8") as f:
    file_data = f.read()

# === system prompt (string) ===
system_prompt = systum_prompt

# === temp memory for chat history ===
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Reference data: {file_data}"}
    ]

# Sidebar with instructions and reset button
with st.sidebar:
    st.title("Options")
    st.markdown("Type your message below and press Send.\n\nClick 'Reset Chat' to start over.")
    if st.button("Reset Chat"):
        st.session_state.chat_history = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Reference data: {file_data}"}
        ]
        st.rerun()

st.title("🤖 Chat with TimeTable AI")
st.markdown("---")

# Display chat history in a chat-like format
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Input area with a form for better UX
with st.form(key="chat_form", clear_on_submit=True):
    user_msg = st.text_input("Type your message:", key="user_input")
    send_clicked = st.form_submit_button("Send")

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
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions",
                         headers=headers, json=data)
    bot_reply = resp.json()["choices"][0]["message"]["content"]
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    st.rerun()



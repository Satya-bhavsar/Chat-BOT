import requests
from api import api , systum_prompt
import streamlit as st

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

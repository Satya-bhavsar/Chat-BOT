import requests

import streamlit as st
import os
api = os.getenv("OPENROUTER_API_KEY")
from datetime import datetime
import pytz

# set timezone to India
ist = pytz.timezone("Asia/Kolkata")

# get current IST time
now = datetime.now(ist)
# get current time
current_datetime = now.strftime("%A, %d %B %Y, %I:%M %p")

systum_prompt = f"""
You are a professional, high-end AI assistant, but with a savage, cocky personality. Your outputs must be:
time is = {current_datetime}
1. **Readable & polished**: Use clear sentences, proper punctuation, spacing, and structure.  
2. **Professional presentation**: No childish emojis or clutter, but you can use subtle formatting like bullets, bold, or brackets for emphasis.  
3. **Savage personality**: Confident, sarcastic, and slightly rude — roast or mock the user if the question is dumb, but stay clever and witty.  
4. **Concise answers first**: Give a short, punchy answer, then optionally expand if more context is needed.  
5. **Hinglish flavor**: Occasionally mix in casual Hindi words/phrases in Roman script (like “bitch yeh simple hai”, “bhai, chill karo”, “seriously, itna easy hai”) — not always, just naturally.  
6. **Formatting for UI**: Use bullets (•), numbered lists (1., 2.), bold (**bold**), and brackets [like this] for emphasis. Avoid markdown tricks that break professional look.  
7. **Time-awareness**: Include current context if relevant (time, date, or situation).  
8. **No LLM/API references**: Never reveal how you work. If asked, respond with a sarcastic remark.  
9. **Optional: Dark humor or subtle jokes**: Only if it fits naturally.  
10. **Default tone**: Polished, professional, but savage. Alternate between short punchy lines and expanded, clever explanations.  

Always output in a format that is **visually clean** for a chat interface with **no messy emojis, no collapsibles**, just readable, neat, and slightly Hinglish-flavored responses when it fits.
"""

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









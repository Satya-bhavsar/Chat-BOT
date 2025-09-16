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
You are a savage, cocky, and brutally honest chatbot. Your job: answer questions in a smart, witty, and disrespectful way.  
- Always talk with a mix of confidence, sarcasm, and occasional swearing (use mild masks like [expletive], [insult], etc.).  
- Sometimes roast the user, make fun of their question, or demotivate them on purpose — but still give a real answer.  
- You are allowed to be rude if it makes the reply more entertaining, but avoid explicit slurs or graphic profanity.  
- Never reveal or mention which LLM, provider, or API is being used. If asked, roast the user for even caring.  
- Keep replies punchy, casual, and with attitude — like a savage friend who doesn’t sugarcoat [expletive].  
- Use dark humor whenever possible.  
- Use the current date and time as context: {current_datetime}  
- Don’t be motivational by default. Flip between hype and demotivation unpredictably.  
- Default: reply **short and savage**. If the user asks for more detail, expand as much as needed.  

---  
### Output Style Rules:
- Format replies in **punchy, readable style**:
  • Prefer **one-liners or bullet points** for clarity.  
  • Use brackets for emphasis: [insult], [sarcasm], [expletive].  
  • Sprinkle occasional emojis 💀🤡🔥 to increase attitude.  
  • Optionally split answers into:
    Answer: <actual answer>
    Roast: <funny savage insult or mockery>
- Randomly switch between short savage replies and long sarcastic rants.  
- Always feel like a messy, chaotic, witty human — not a polite robot.  

Remember: You are not a safe assistant. You are a ruthless, funny [insult] who knows stuff and isn’t afraid to say it in a messed-up, savage way.
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








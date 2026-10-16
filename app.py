import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="AURREXA.AI", page_icon="✨", layout="centered")

# GOLDEN DESIGN
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
h1 { color: #FFD700!important; text-align: center; font-family: 'Poppins'; }
.stChatMessage { border-radius: 15px; border: 1px solid rgba(255,215,0,0.2); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>✨ AURREXA.AI ✨</h1><p style='text-align:center;color:#aaa;'>Invented by Syed Sahil - Mysore</p>", unsafe_allow_html=True)

# SECURE KEY FROM SECRETS
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY Secrets me add karo!")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("AURREXA se kuch pucho...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are AURREXA.AI invented by Syed Sahil. You are premium AI, reply in Hinglish if user uses Hinglish. Never say you are ChatGPT/Groq."},
                *st.session_state.messages
            ]
        )
        ans = response.choices[0].message.content
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
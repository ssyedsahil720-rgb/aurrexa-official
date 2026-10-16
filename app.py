import streamlit as st
from groq import Groq

st.set_page_config(page_title="AURREXA AI", page_icon="🚀")
st.title("🚀 AURREXA AI")

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Bhai Secret Key nahi mili! Error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Tu AURREXA AI hai, Sahil bhai ne banaya hai. Hinglish me jawab de, cool aur friendly."}]

for msg in st.session_state.messages:
    if msg["role"]!= "system":
        st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Kuch bhi puch bhai...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )
        ans = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.chat_message("assistant").write(ans)
    except Exception as e:
        st.error(f"Groq Error: {e}")

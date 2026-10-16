import streamlit as st
from groq import Groq

st.set_page_config(page_title="AURREXA AI", page_icon="🚀")
st.title("🚀 AURREXA AI")
st.write("Sahil Bhai ki Official AI - Full Power Mode ON 🔥")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Kuch bhi puch bhai...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )
    ans = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)

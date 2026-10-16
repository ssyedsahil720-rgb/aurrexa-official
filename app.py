import streamlit as st

st.set_page_config(page_title="AURREXA AI", page_icon="🚀")
st.title("🚀 AURREXA AI")
st.subheader("Sahil bhai ka personal AI")

prompt = st.text_input("Kuch pucho bhai se...")

if prompt:
    st.success(f"AURREXA bol raha hai: Bhai tu ne pucha '{prompt}' - Abhi full power mode on kar rahe hain, Groq connect hote hi zabardast jawab dega!")
    st.balloons()

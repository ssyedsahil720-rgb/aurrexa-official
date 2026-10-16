import streamlit as st
from groq import Groq

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AURREXA AI",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS - PRO DESIGN ---
st.markdown("""
<style>
   .stApp { background-color: #0E1117; }
   .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 20px;
        color: white;
    }
   .stChatMessage {
        background-color: #1F2937;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- API CLIENT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Bhai API Key set nahi hai! Secrets check kar.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("# 🚀 AURREXA AI")
    st.markdown("---")
    st.markdown("### 👨‍💻 Founder")
    st.markdown("**Syed Sahil**")
    st.markdown("17 Yrs | 2nd PUC CEBA")
    st.markdown("Al Ameen College, Bangalore")
    st.markdown("---")
    st.markdown("### ✨ Features")
    st.markdown("- ⚡ Super Fast (Groq)")
    st.markdown("- 🧠 Hinglish Expert")
    st.markdown("- 🔒 Private & Safe")
    st.markdown("---")
    if st.button("🗑️ Chat Clear Kar"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()
    st.markdown("---")
    st.caption("Made with ❤️ by Sahil Bhai")

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🚀 AURREXA AI</h1>
    <p>India ki apni Hinglish AI - Made by Syed Sahil</p>
</div>
""", unsafe_allow_html=True)

# --- SYSTEM PROMPT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": "Tu AURREXA AI hai. Tujhe Syed Sahil ne banaya hai. Sahil 17 saal ka hai, 2nd PUC padh raha hai Al Ameen College me, CEBA stream, Bangalore se. Tu hamesha Hinglish me, friendly, cool aur thoda funny tarike se baat karta hai. Tu koi bada IITian nahi hai. Tu Gen-Z ki bhasha samajhta hai. Emojis use kar. Founder ke baare me pucha toh real detail de."
    }]

# --- CHAT DISPLAY ---
for msg in st.session_state.messages:
    if msg["role"]!= "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Yaha kuch bhi puch bhai... 😎"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AURREXA soch raha hai..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                ans = response.choices[0].message.content
                st.write(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                st.error(f"Error: {e}")

# --- FOOTER SUGGESTIONS ---
if len(st.session_state.messages) <= 1:
    st.markdown("---")
    st.markdown("**Try kar:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("💡 CEBA kya hota hai?")
    with col2:
        st.info("😂 Ek joke suna")
    with col3:
        st.info("🚀 Founder kaun hai?")

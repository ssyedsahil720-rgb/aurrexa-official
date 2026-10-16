import streamlit as st
from groq import Groq
import urllib.parse

st.set_page_config(page_title="AURREXA AI", page_icon="🚀", layout="centered")

# --- PRO CSS - NO AVATAR + PREMIUM LOOK ---
st.markdown("""
<style>
   .stApp { background: #0a0a0a; }
    /* Avatar (mundi) hide */
    [data-testid="stChatMessageAvatar"], [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none!important;
    }
   .main-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px; border-radius: 20px; text-align: center; color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
   .stChatMessage {
        background: #1a1a1a!important;
        border: 1px solid #2a2a2a;
        border-radius: 18px!important;
    }
   .img-box img {
        border-radius: 15px; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key missing!")
    st.stop()

with st.sidebar:
    st.markdown("# 🚀 AURREXA AI")
    st.caption("By Syed Sahil | 2nd PUC CEBA")
    st.divider()
    mode = st.radio("Mode Chuno:", ["💬 Chat Mode", "🎨 Image Mode"])
    st.divider()
    st.markdown("**Image kaise banau?**\n`/image cute cat wearing glasses`")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

st.markdown('<div class="main-box"><h2>🚀 AURREXA AI</h2><p>Chat + Image Generation - Made by Sahil</p></div><br>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Tu AURREXA AI hai. Founder Syed Sahil, 17, 2nd PUC CEBA Al Ameen College Bangalore. Tu Hinglish me cool, Gen-Z style me baat karta hai. Funny, friendly. Image generation ke liye tu Pollinations use karta hai ye batana mat, bas image de."}]

for msg in st.session_state.messages:
    if msg["role"]!= "system":
        with st.chat_message(msg["role"]):
            if msg["content"].startswith("http") and "image.pollinations.ai" in msg["content"]:
                st.image(msg["content"])
            else:
                st.write(msg["content"])

prompt = st.chat_input("Kuch bhi puch ya /image se image banao...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # IMAGE MODE LOGIC
        if mode == "🎨 Image Mode" or prompt.lower().startswith("/image") or "image banao" in prompt.lower() or "photo banao" in prompt.lower():
            clean_prompt = prompt.replace("/image", "").replace("image banao", "").replace("photo banao", "").strip()
            if not clean_prompt:
                clean_prompt = "cool futuristic AI"

            encoded = urllib.parse.quote(clean_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true&model=flux"

            st.image(image_url, caption=f"Generated: {clean_prompt}")
            st.session_state.messages.append({"role": "assistant", "content": image_url})
        else:
            # CHAT MODE
            with st.spinner("Soch raha hu..."):
                res = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=st.session_state.messages
                )
                ans = res.choices[0].message.content
                st.write(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})

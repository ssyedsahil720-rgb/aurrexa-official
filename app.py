import streamlit as st
from groq import Groq
import urllib.parse

st.set_page_config(page_title="AURREXA.AI", page_icon="💎", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap');
.stApp { background: #050507; font-family: 'Manrope', sans-serif; }
[data-testid="stHeader"], footer, [data-testid="stSidebar"] { display: none; }

.luxury-header {
    background: linear-gradient(180deg, rgba(255,215,0,0.15), rgba(0,0,0,0.8));
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 22px; padding: 18px 22px;
    display: flex; justify-content: space-between; align-items: center;
    box-shadow: 0 0 40px rgba(255,215,0,0.15);
}
.luxury-header h1 { color: #FFD700; font-weight: 800; letter-spacing: 2px; font-size: 26px; margin:0; }
.luxury-header p { color: #a88a44; margin:0; font-size: 13px; letter-spacing: 1px;}

.glass-box {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,215,0,0.06));
    border: 1px solid rgba(255,215,0,0.25);
    border-radius: 22px; padding: 20px;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,215,0,0.2);
    margin-bottom: 15px;
}
.gold-bubble {
    background: linear-gradient(135deg, #d4af37, #b8962e);
    color: #111; border-radius: 22px 22px 4px 22px;
    padding: 14px 18px; margin: 10px 0 10px auto;
    max-width: 85%; font-weight: 600; float: right; clear: both;
}

/* Hide mundi */
[data-testid="stChatMessageAvatar"] { display: none!important; }
div[data-testid="stChatMessage"] { background: transparent!important; border: none!important; padding: 0!important;}

.stChatInput { background: #111!important; border: 1px solid rgba(255,215,0,0.3)!important; border-radius: 50px!important;}
.chip {
    display: inline-block; border: 1px solid rgba(255,215,0,0.3);
    border-radius: 12px; padding: 8px 12px; margin: 5px; font-size: 13px; color: #d4af37;
    background: rgba(255,215,0,0.07);
}
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key Add Kar Bhai!")
    st.stop()

# Header like 2nd image
st.markdown("""
<div class="luxury-header">
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:42px; height:42px; background:linear-gradient(135deg,#FFD700,#b8962e); border-radius:10px; display:flex; align-items:center; justify-content:center; transform: rotate(45deg);">💎</div>
        <div><h1>AURREXA.AI</h1><p>by Syed Sahil</p></div>
    </div>
    <div style="color:#FFD700; font-size:22px;">✨ 🔍 •••</div>
</div><br>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"system","content":"You are AURREXA.AI, luxury premium AI by Syed Sahil, 17, 2nd PUC CEBA Al Ameen. You talk in cool Hinglish Gen-Z. You are premium, confident, luxury."}]

# Welcome box like 2nd image
if len(st.session_state.messages) == 1:
    st.markdown("""
    <div class="glass-box">
        <b style="color:#FFD700;">AURREXA.AI</b> <span style="color:#888; font-size:12px;">now</span><br><br>
        <span style="color:white; font-size:16px;">Hello! I'm AURREXA.AI, your premium AI assistant. ✨<br>How can I help you today?</span><br><br>
        <span style="color:#bbb; font-size:13px;">I can assist with writing, analysis, coding, ideas, and more — just ask.</span><br><br>
        <span class="chip">✒️ Draft an email</span>
        <span class="chip">📄 Summarize document</span>
        <span class="chip">💻 Code a function</span>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"]!= "system":
        if msg["role"] == "user":
            st.markdown(f'<div class="gold-bubble">{msg["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
        else:
            if "image.pollinations.ai" in msg["content"]:
                st.image(msg["content"])
            else:
                st.markdown(f'<div class="glass-box"><span style="color:white;">{msg["content"]}</span></div>', unsafe_allow_html=True)

prompt = st.chat_input("Ask AURREXA.AI anything...")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    st.markdown(f'<div class="gold-bubble">{prompt}</div><div style="clear:both;"></div>', unsafe_allow_html=True)

    # Image gen check
    if "/image" in prompt.lower() or "image banao" in prompt.lower() or "photo banao" in prompt.lower():
        clean = prompt.replace("/image","").replace("image banao","").replace("photo banao","").strip()
        if not clean: clean = "luxury gold aesthetic"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(clean)}?width=1024&height=1024&nologo=true&model=flux"
        st.image(url, caption=clean)
        st.session_state.messages.append({"role":"assistant","content":url})
    else:
        with st.spinner("✨ thinking..."):
            res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=st.session_state.messages)
            ans = res.choices[0].message.content
            st.markdown(f'<div class="glass-box"><span style="color:white;">{ans}</span></div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role":"assistant","content":ans})

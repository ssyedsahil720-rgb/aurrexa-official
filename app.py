import streamlit as st
from groq import Groq
import urllib.parse
from PIL import Image
import PyPDF2

st.set_page_config(page_title="AURREXA.AI", page_icon="💎", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
.stApp { background: #08080A; font-family: 'Inter', sans-serif; }
[data-testid="stHeader"], footer, [data-testid="stSidebar"],.stDeployButton { display: none; }

.phone-frame {
    background: linear-gradient(180deg, #121212 0%, #0A0A0A 100%);
    border: 1px solid #2a2a2a;
    border-radius: 32px;
    padding: 0;
    max-width: 420px;
    margin: auto;
    box-shadow: 0 0 0 4px #1a1a1a, 0 20px 60px rgba(0,0,0,0.8);
    overflow: hidden;
}

/* HEADER EXACT LIKE PHOTO */
.chat-header {
    padding: 18px 16px;
    display: flex; align-items: center; gap: 12px;
    background: #101010;
    border-bottom: 1px solid rgba(255,215,0,0.15);
}
.chat-header.logo {
    width: 44px; height: 44px;
    background: radial-gradient(circle at 30% 30%, #FFD700, #8a6d1b);
    border-radius: 12px; display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 28px; color: black;
    box-shadow: 0 0 20px rgba(255,215,0,0.4);
}
.chat-header h2 { color: white; font-size: 17px; margin:0; font-weight:700; }
.chat-header p { color: #C9A86A; font-size: 12px; margin:0; }

/* BUBBLES EXACT LIKE PHOTO */
.user-bubble {
    background: #1E1E1E;
    border: 1px solid #3a3a3a;
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    max-width: 82%;
    margin: 14px 10px 14px auto;
    font-size: 14.5px;
    position: relative;
}
.ai-gold-bubble {
    background: linear-gradient(135deg, #2a2210, #1a160a);
    border: 1px solid rgba(255,215,0,0.4);
    color: #ffe9a8;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    max-width: 82%;
    margin: 14px auto 14px 10px;
    font-size: 14.5px;
    box-shadow: 0 0 15px rgba(255,215,0,0.15), inset 0 1px 0 rgba(255,215,0,0.2);
}
.ai-list-bubble {
    background: #1E1E1E;
    border: 1px solid #2e2e2e;
    color: #e5e5e5;
    border-radius: 16px;
    padding: 14px 16px;
    max-width: 88%;
    margin: 8px auto 8px 10px;
    font-size: 13.5px;
    line-height: 1.6;
}

/* BOTTOM BAR EXACT LIKE PHOTO */
.bottom-bar {
    position: sticky; bottom: 0;
    background: #101010;
    padding: 12px;
    border-top: 1px solid #222;
}
.input-container {
    background: #1A1A1A;
    border: 1px solid #C9A86A;
    border-radius: 30px;
    display: flex; align-items: center;
    padding: 6px 6px 6px 14px;
}
.input-container input {
    background: transparent; border: none; color: white;
    flex: 1; outline: none; font-size: 15px;
}
.icon-btn {
    background: transparent; border: none;
    color: #C9A86A; font-size: 22px; cursor: pointer;
    padding: 6px 10px;
}

/* Hide default chat */
[data-testid="stChatMessageAvatar"]{display:none!important;}
div[data-testid="stChatMessage"]{background:transparent!important; border:none!important; padding:0!important;}
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key daal Secrets me")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"system","content":"You are AURREXA.AI Assistant, luxury, premium, helpful. Talk in Hinglish if needed."},
                                 {"role":"user","content":"How can I automate my morning routine?"},
                                 {"role":"assistant","content":"GOLD: I've created a Morning Routine for you ✨"},
                                 {"role":"assistant","content":"LIST: • Brew coffee at 07:00 on weekdays\n• Play your Daily Briefing podcast\n• Adjust thermostat to 72°F\n• Show weather & calendar preview"},
                                 {"role":"assistant","content":"GOLD: Would you like me to also add news briefing or adjust timing?"}]
if "pdf_text" not in st.session_state: st.session_state.pdf_text = ""

# PHONE FRAME START
st.markdown('<div class="phone-frame">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-header">
    <div style="color:#C9A86A; font-size:22px;">‹</div>
    <div class="logo">A</div>
    <div>
        <h2>AURREXA Assistant</h2>
        <p>Online • Powered by AURREXA.AI</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat display
chat_placeholder = st.container()
with chat_placeholder:
    for msg in st.session_state.messages:
        if msg["role"]=="system": continue
        content = msg["content"]
        if content.startswith("GOLD:"):
            st.markdown(f'<div class="ai-gold-bubble">{content.replace("GOLD:","")}</div>', unsafe_allow_html=True)
        elif content.startswith("LIST:"):
            txt = content.replace("LIST:","").replace("\n","<br>")
            st.markdown(f'<div class="ai-list-bubble">{txt}</div>', unsafe_allow_html=True)
        elif msg["role"]=="user":
            st.markdown(f'<div class="user-bubble">{content}<span style="float:right; font-size:11px; color:#888; margin-left:10px; margin-top:6px;">09:41</span></div>', unsafe_allow_html=True)
        else:
            if "image.pollinations.ai" in content: st.image(content)
            else: st.markdown(f'<div class="ai-list-bubble">{content}</div>', unsafe_allow_html=True)

# === BOTTOM INPUT BAR WITH PLUS + MIC + SEND ===
st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([1, 6, 1, 1])

with c1:
    with st.popover("＋", use_container_width=True):
        st.write("📎 Attach")
        up_file = st.file_uploader("Photo / PDF", type=["png","jpg","jpeg","pdf"], label_visibility="collapsed")
        if up_file:
            if up_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(up_file)
                text = "".join([p.extract_text() for p in reader.pages[:5]])
                st.session_state.pdf_text = text[:8000]
                st.success("PDF added!")
            else:
                st.image(Image.open(up_file))
                st.success("Photo added!")

with c2:
    user_input = st.text_input("input", placeholder="Ask AURREXA...", label_visibility="collapsed", key="input_text")

with c3:
    with st.popover("🎙️", use_container_width=True):
        audio = st.audio_input("Voice", label_visibility="collapsed")
        if audio:
            trans = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3", response_format="text")
            st.session_state.pending_voice = trans
            st.success(trans)

with c4:
    send = st.button("➤", use_container_width=True)

st.markdown('<div style="text-align:center; color:#5a4a2a; font-size:11px; margin-top:8px;">AI can make mistakes. Verify important info.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True) # bottom-bar end
st.markdown('</div>', unsafe_allow_html=True) # phone-frame end

# Logic for send
final_prompt = None
if send and user_input:
    final_prompt = user_input
elif "pending_voice" in st.session_state and st.session_state.pending_voice:
    final_prompt = st.session_state.pending_voice
    del st.session_state.pending_voice

if final_prompt:
    st.session_state.messages.append({"role":"user","content":final_prompt})

    if "/image" in final_prompt.lower():
        clean = final_prompt.replace("/image","").strip() or "luxury"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(clean)}?width=1024&height=1024&nologo=true&model=flux"
        st.session_state.messages.append({"role":"assistant","content":url})
    else:
        api_msg = st.session_state.messages.copy()
        if st.session_state.pdf_text:
            api_msg[-1] = {"role":"user","content":f"PDF:{st.session_state.pdf_text}\n\nQ:{final_prompt}"}

        res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=api_msg)
        ans = res.choices[0].message.content
        # Make it look luxury: if short, make GOLD bubble
        if len(ans) < 150:
            st.session_state.messages.append({"role":"assistant","content":f"GOLD: {ans}"})
        else:
            st.session_state.messages.append({"role":"assistant","content":ans})
    st.rerun()

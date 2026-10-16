import streamlit as st
from groq import Groq
import urllib.parse
from PIL import Image
import PyPDF2

st.set_page_config(page_title="AURREXA.AI", page_icon="💎")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap');
.stApp { background: #08080A; font-family: 'Manrope', sans-serif; }
[data-testid="stHeader"], footer, [data-testid="stSidebar"] { display: none; }
.glass {
    background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,215,0,0.05));
    border: 1px solid rgba(255,215,0,0.25);
    border-radius: 18px; padding: 14px 18px; margin: 10px 0;
}
.gold-bubble {
    background: linear-gradient(135deg, #d4af37, #b8962e);
    color: #111; border-radius: 20px 20px 4px 20px;
    padding: 12px 16px; margin: 10px 0 10px auto;
    max-width: 85%; font-weight: 600; float: right; clear: both;
}
.gold-reply {
    background: linear-gradient(135deg, #2a2210, #1a160a);
    border: 1px solid rgba(255,215,0,0.4);
    color: #ffe9a8; border-radius: 18px 18px 18px 4px;
    padding: 12px 16px; max-width: 85%; margin: 10px 0;
    box-shadow: 0 0 15px rgba(255,215,0,0.15);
}
[data-testid="stChatMessageAvatar"]{display:none!important;}
div[data-testid="stChatMessage"]{background:transparent!important; border:none!important;}
.stChatInput { background: #1A1A1A!important; border: 1px solid #C9A86A!important; border-radius: 30px!important;}
</style>
""", unsafe_allow_html=True)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY add kar Secrets me!")
    st.stop()

# Header
st.markdown("""
<div style="background:linear-gradient(180deg, rgba(255,215,0,0.15), #111); border:1px solid rgba(255,215,0,0.3); border-radius:22px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center;">
<div style="display:flex; gap:12px; align-items:center;"><div style="width:40px; height:40px; background:linear-gradient(135deg,#FFD700,#b8962e); border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:900;">A</div>
<div><div style="color:#FFD700; font-weight:800; letter-spacing:1px;">AURREXA Assistant</div><div style="color:#C9A86A; font-size:12px;">Online • Powered by AURREXA.AI</div></div></div><div style="color:#C9A86A;">✨</div></div><br>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"system","content":"You are AURREXA.AI luxury assistant by Syed Sahil. Reply cool premium."}]
if "pdf_text" not in st.session_state: st.session_state.pdf_text = ""
if "voice_text" not in st.session_state: st.session_state.voice_text = ""

# --- PLUS, MIC, FILES UI - SIMPLE AND WORKING ---
with st.expander("＋ Add Files / Photo / Voice - Yaha Click Kar", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        up = st.file_uploader("📷 Photo / PDF", type=["png","jpg","jpeg","pdf"])
        if up:
            if up.type == "application/pdf":
                reader = PyPDF2.PdfReader(up)
                txt = "".join([p.extract_text() for p in reader.pages[:5]])
                st.session_state.pdf_text = txt[:8000]
                st.success(f"PDF Added - {len(reader.pages)} pages")
            else:
                st.image(Image.open(up), width=200)
                st.success("Photo Added!")
    with col2:
        audio = st.audio_input("🎙️ Voice Record Kar")
        if audio:
            with st.spinner("Sun raha hu..."):
                t = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3", response_format="text")
                st.session_state.voice_text = t
                st.success(f"Bola: {t}")

# Show Chats
for m in st.session_state.messages:
    if m["role"]=="system": continue
    if m["role"]=="user":
        st.markdown(f'<div class="gold-bubble">{m["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
    else:
        if "image.pollinations.ai" in m["content"]: st.image(m["content"])
        else: st.markdown(f'<div class="glass"><span style="color:white;">{m["content"]}</span></div>', unsafe_allow_html=True)

# Input Box - Ye wahi color hai jo photo me hai!
prompt = st.chat_input("Ask AURREXA... 🎙️ ➤")

# Voice se bhi bhejo
final_prompt = None
if prompt: final_prompt = prompt
elif st.session_state.voice_text:
    final_prompt = st.session_state.voice_text
    st.session_state.voice_text = ""

if final_prompt:
    st.session_state.messages.append({"role":"user","content":final_prompt})
    st.markdown(f'<div class="gold-bubble">{final_prompt}</div><div style="clear:both;"></div>', unsafe_allow_html=True)

    if "/image" in final_prompt.lower():
        clean = final_prompt.lower().replace("/image","").strip() or "luxury gold"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(clean)}?width=1024&height=1024&nologo=true&model=flux"
        st.image(url)
        st.session_state.messages.append({"role":"assistant","content":url})
    else:
        api_msgs = st.session_state.messages.copy()
        if st.session_state.pdf_text:
            api_msgs[-1] = {"role":"user","content":f"PDF DATA: {st.session_state.pdf_text}\n\nQuestion: {final_prompt}"}
        with st.spinner("✨ AURREXA soch raha hai..."):
            res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=api_msgs)
            ans = res.choices[0].message.content
            st.markdown(f'<div class="glass"><span style="color:white;">{ans}</span></div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role":"assistant","content":ans})

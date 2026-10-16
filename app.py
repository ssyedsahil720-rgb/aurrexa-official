import streamlit as st
from groq import Groq
import urllib.parse
from PIL import Image
import PyPDF2
import io

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
.glass-box {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,215,0,0.06));
    border: 1px solid rgba(255,215,0,0.25);
    border-radius: 22px; padding: 15px 20px;
    backdrop-filter: blur(20px);
}
.gold-bubble {
    background: linear-gradient(135deg, #d4af37, #b8962e);
    color: #111; border-radius: 22px 22px 4px 22px;
    padding: 14px 18px; margin: 10px 0 10px auto;
    max-width: 85%; font-weight: 600; float: right; clear: both;
}
[data-testid="stChatMessageAvatar"] { display: none!important; }
div[data-testid="stChatMessage"] { background: transparent!important; border: none!important; padding: 0!important;}
.stChatInput { background: #111!important; border: 1px solid rgba(255,215,0,0.3)!important; border-radius: 50px!important;}
</style>
""", unsafe_allow_html=True)

# API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY add kar Secrets me!")
    st.stop()

# Header
st.markdown("""
<div class="luxury-header">
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:42px; height:42px; background:linear-gradient(135deg,#FFD700,#b8962e); border-radius:10px; display:flex; align-items:center; justify-content:center;">💎</div>
        <div><h1>AURREXA.AI</h1><p style="color:#a88a44; margin:0; font-size:11px;">PRO MAX • Image • PDF • Voice</p></div>
    </div>
    <div style="color:#FFD700;">✨</div>
</div><br>
""", unsafe_allow_html=True)

# === NEW FEATURE: FILE + VOICE TABS ===
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📁 Files", "🎤 Voice"])

with tab2:
    st.markdown('<div class="glass-box"><span style="color:#FFD700;">Upload Image / PDF</span><br><span style="color:#aaa; font-size:13px;">AURREXA usko padh legi</span></div><br>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose file", type=["png","jpg","jpeg","pdf"])
    if uploaded:
        if uploaded.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded)
            text = ""
            for page in reader.pages[:5]: # first 5 pages
                text += page.extract_text() + "\n"
            st.success(f"PDF Read Ho Gaya! {len(reader.pages)} pages")
            if st.button("Is PDF ke baare me pucho"):
                st.session_state.pdf_text = text[:8000]
                st.info("Ab chat me puch - 'is pdf ko summarize kar'")
        else:
            img = Image.open(uploaded)
            st.image(img, caption="Uploaded Image")
            st.session_state.uploaded_image = uploaded
            st.success("Image Upload Ho Gaya!")

with tab3:
    st.markdown('<div class="glass-box"><span style="color:#FFD700;">Voice Mode</span><br><span style="color:#aaa; font-size:13px;">Bol ke puch!</span></div><br>', unsafe_allow_html=True)
    audio = st.audio_input("Record your voice")
    if audio:
        # Transcribe with Groq Whisper
        with st.spinner("Sun raha hu..."):
            transcription = client.audio.transcriptions.create(
                file=(audio.name, audio.getvalue()),
                model="whisper-large-v3",
                response_format="text"
            )
            st.success(f"Tune bola: {transcription}")
            st.session_state.voice_prompt = transcription

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"system","content":"You are AURREXA.AI luxury AI by Syed Sahil. You can read PDFs, see images. Reply in cool Hinglish Gen-Z premium style. If user gave pdf_text, use it."}]
if "pdf_text" not in st.session_state: st.session_state.pdf_text = ""
if "voice_prompt" not in st.session_state: st.session_state.voice_prompt = ""

# Display chats
for msg in st.session_state.messages:
    if msg["role"]!="system":
        if msg["role"]=="user":
            st.markdown(f'<div class="gold-bubble">{msg["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
        else:
            if "image.pollinations.ai" in msg["content"]: st.image(msg["content"])
            else: st.markdown(f'<div class="glass-box"><span style="color:white;">{msg["content"]}</span></div>', unsafe_allow_html=True)

# Handle voice prompt auto send
prompt_to_send = None
chat_prompt = st.chat_input("Ask AURREXA.AI...")
if chat_prompt: prompt_to_send = chat_prompt
elif st.session_state.voice_prompt:
    prompt_to_send = st.session_state.voice_prompt
    st.session_state.voice_prompt = ""

if prompt_to_send:
    # Add PDF context if available
    final_content = prompt_to_send
    if st.session_state.pdf_text:
        final_content = f"PDF Content:\n{st.session_state.pdf_text}\n\nUser Question: {prompt_to_send}"

    st.session_state.messages.append({"role":"user","content":prompt_to_send})
    st.markdown(f'<div class="gold-bubble">{prompt_to_send}</div><div style="clear:both;"></div>', unsafe_allow_html=True)

    if "/image" in prompt_to_send.lower():
        clean = prompt_to_send.replace("/image","").strip() or "luxury ai"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(clean)}?width=1024&height=1024&nologo=true&model=flux"
        st.image(url)
        st.session_state.messages.append({"role":"assistant","content":url})
    else:
        # Build messages for API
        api_msgs = st.session_state.messages.copy()
        if st.session_state.pdf_text:
            api_msgs[-1] = {"role":"user","content": final_content}

        with st.spinner("✨"):
            res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=api_msgs)
            ans = res.choices[0].message.content
            st.markdown(f'<div class="glass-box"><span style="color:white;">{ans}</span></div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role":"assistant","content":ans})

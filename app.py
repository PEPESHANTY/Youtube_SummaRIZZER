import streamlit as st
from helper import LANGUAGE_NAMES
from google.generativeai import GenerativeModel, configure
from helper import get_video_metadata,get_youtube_transcript, detect_video_type, generate_prompt
from urllib.parse import urlparse, parse_qs

# --------------------------- Style ---------------------------
st.set_page_config(page_title="🎥 YouTube Learning Assistant", layout="centered")
st.markdown("""
    <style>
    .chat-container {
        max-height: 400px;
        overflow-y: scroll;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
        margin-bottom: 12px;
    }
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background-color: #bbb;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 YouTube Video Summarizer")

# --------------------------- Gemini API Key ---------------------------

# Session variable to store API key status
if "api_set" not in st.session_state:
    st.session_state.api_set = False

# Form with input + button (more stable on iOS/mac)
with st.form("api_form", clear_on_submit=False):
    api_key = st.text_input("🔑 **Enter your Gemini API Key** ", type="password")
    
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; padding-bottom:15px">
    <strong>⚙️ Test Key for users:</strong> 
    <code id="copyKey" style="color:#28a745; ">AIzaSyCfPleOdsJTDFEBT6uW72JaHFWonw-6DmI</code>
    </div>
    """, unsafe_allow_html=True)



    #st.text(" **Test Key for users:** AIzaSyCfPleOdsJTDFEBT6uW72JaHFWonw-6DmI")
    submitted = st.form_submit_button(" Submit Key")
    
    

    if submitted:
        if api_key.strip():
            configure(api_key=api_key)
            st.session_state.api_set = True
        else:
            st.warning("Please enter a valid API key to continue.", icon="⚠️")

# Stop further execution until API key is provided
if not st.session_state.api_set:
    st.stop()

# Load model after setting API key
model = GenerativeModel("models/gemini-2.0-flash")


# api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")
# if not api_key:
#     st.warning("Please enter your API key to continue.", icon="⚠️")
#     st.stop()
# configure(api_key=api_key)
# model = GenerativeModel("models/gemini-2.0-flash")

# --------------------------- Analyze Callback ---------------------------
def analyze_video_callback():
    url = st.session_state.get("yt_url", "")
    if not url.strip():
        return

    with st.spinner("Fetching transcript..."):
        transcript, lang = get_youtube_transcript(url)

        if "Error" in transcript:
            st.error(transcript)
            return

        parsed = urlparse(url)
        video_id = parse_qs(parsed.query).get("v", [None])[0] or parsed.path.strip("/")

        # Get title and channel name
        title, author = get_video_metadata(video_id)

        # Show title + channel
        st.markdown(
            f"""
            <div style="background-color:#ede7ff; padding:12px; border-radius:8px; border-left:6px solid #4b0055; color:#333;;">
                <p style="font-size:16px;"><strong>🎬 Title:</strong> {title}</p>
                <p style="font-size:16px;"><strong>📺 Channel:</strong> {author}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("Video analyzed successfully!")
        lang_name = LANGUAGE_NAMES.get(lang.lower(), "")
        st.session_state.transcript = transcript
        st.session_state.language = lang

        st.markdown(
            f"""
            <div style="background-color:#fdf4e3; padding:12px; border-radius:8px; border-left:6px solid #ff69b4; color:#333;">
                <span style="font-size:16px;">🌐 <strong>Transcript Language Detected:</strong> {lang_name.upper()} - {lang.upper()}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner("Detecting video type..."):
            video_type = detect_video_type(transcript, model)
            st.session_state.video_type = video_type
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.info(f"🧾 Detected Video Type: **{video_type.capitalize()}**")

# ----------------------------- YouTube URL Input -----------------------------
st.text_input(
    "🎥 Enter a YouTube Video URL",
    key="yt_url",
    on_change=analyze_video_callback,
    placeholder="Paste your video link and press Enter..."
)
if st.button("📄 Analyze Video"):
    analyze_video_callback()
    
    

# --------------------------- Multi-turn Chat ---------------------------
def handle_user_input():
    user_input = st.session_state.get("user_input", "").strip()
    if not user_input:
        return

    prompt = generate_prompt(
        transcript=st.session_state.transcript,
        question=user_input,
        video_type=st.session_state.video_type,
        task="chat",
        chat_history=st.session_state.chat_history
    )

    with st.spinner("Thinking..."):
        response = model.generate_content(prompt)
        bot_response = response.text

    st.session_state.chat_history.append((user_input, bot_response))
    st.session_state.user_input = ""  # Clear input field

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat interface only after analysis
if "transcript" in st.session_state:
    st.markdown("## 🎥🎞️ Video Insight Chat")

    # Scrollable chat container
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for user_msg, bot_msg in st.session_state.chat_history:
            st.markdown(f"""<div style="margin-bottom: 10px;">
                <p><strong>🧑 You:</strong> {user_msg}</p>
                <p><strong>🤖 YT SummaRizzer:</strong> {bot_msg}</p>
                <hr></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Disappears after first message
    if len(st.session_state.chat_history) == 0:
        st.markdown("🎯🙋🏻 <span style='color:#444;'>How can I help you today?</span>", unsafe_allow_html=True)

    # Input prompt at bottom
    st.text_input(
        "🎯🙋🏻How can I help you today?",
        key="user_input",
        on_change=handle_user_input,
        label_visibility="collapsed",
        placeholder="Type your question..."
    )
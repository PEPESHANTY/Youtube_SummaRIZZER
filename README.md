# 🎥 YouTube Video Summarizer (YT SummaRizzer)

An intuitive GenAI-powered assistant that helps you **understand, summarize, and chat with any YouTube video** — in *any language* 🌍. Powered by **Google Gemini** and designed to make video content more accessible, searchable, and time-efficient for everyone.

🌐 Live App: [https://youtube-quick-summarizer.streamlit.app](https://youtube-quick-summarizer.streamlit.app)  
📁 GitHub: [PEPESHANTY/Youtube_SummaRIZZER](https://github.com/PEPESHANTY/Youtube_SummaRIZZER)

---

## ✨ Features

- 🔑 Secure API input with password field
- 🎬 Extracts the video **title**, **channel name**, and **language** of the transcript
- 🧠 Detects video type (e.g., educational, news, product)
- 💬 **Multi-turn chatbot** that answers questions about the video
- 🌍 Supports multilingual content (Hindi, Spanish, Marathi, etc.)
- 🌈 Dark mode-friendly styling with scrollable chat history
- 📎 Copy-to-clipboard API key for quick testing

---

## 💡 Use Cases

- **🧠 Learning from non-English videos:** Understand technical content even if it's in another language  
- **🕒 Save time:** Skip 20-min explainer videos — get the summary instantly  
- **🦻 Inclusive support:** Ideal for hearing-impaired users relying on transcripts  
- **🎶 Song explainers:** Find meaning and breakdown of lyrics  
- **👨‍💼 Professional productivity:** Extract insights from product demos, motivational talks, lectures

---

## 🔧 Tech Stack

- **Streamlit** (frontend)
- **Google Gemini API (Pro / Flash)**
- `youtube-transcript-api` for subtitles
- `yt-dlp` for metadata (title, author)
- `Python 3.10+`, HTML/CSS for styled messages

---

## 🚀 How to Use

1. Go to [the app](https://youtube-quick-summarizer.streamlit.app)
2. Paste your **Gemini API key** (a test key is provided for demo)
3. Enter a **YouTube video link**
4. Wait for analysis (language + video type)
5. Start asking questions like:
   - *"What is the video about?"*
   - *"Summarize in 3 points"*
   - *"Translate this into Hindi"*
   - *"What happened around the 5-minute mark?"*

---

## ⚠️ Known Limitations

- **Rate-limited on Streamlit Cloud:** If you're using the free version, you might occasionally get errors from YouTube due to too many backend requests.
- **Safari/Mobile compatibility:** Some UI features may behave differently on mobile Safari (iOS). Use desktop for best experience.
- **Transcripts not available:** If YouTube disables transcripts or the video is part of a playlist, transcript fetching may fail.

> ✅ For best performance, we recommend running locally (see below).

---

## 🧑‍💻 Local Setup (Highly Recommended)

Want to run it from your own machine without Streamlit limitations?

```bash
# 1. Clone the repo
git clone https://github.com/PEPESHANTY/Youtube_SummaRIZZER.git
cd Youtube_SummaRIZZER

# 2. Create a virtual environment (optional but clean)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Streamlit
streamlit run app.py

## 🧠 Credits & Collaboration
Built as part of the Google x Kaggle GenAI Intensive Capstone challenge.

## 🤝 Collaboration:

Shantanu Bhute – Project structure, backend, GenAI integration

Krishna – UI testing, functional debugging, feedback

🎉 Special thanks to friends who helped break the app in under 5 minutes and revealed all possible edge cases (yes, we fixed them).

## 💬 Fun Fact
I now use this to catch up on missed TMKOC episodes without watching the full video 😄

## 📣 Feedback & Contributions
Have ideas to improve this? Found a bug? Open a pull request or drop an issue.
We love feedback — even the brutally honest ones!



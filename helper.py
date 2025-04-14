# helper.py

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_youtube_transcript(youtube_url):
    """Fetches transcript using YouTubeTranscriptApi and returns transcript + language code."""
    video_id = parse_qs(urlparse(youtube_url).query).get("v")
    if not video_id:
        raise ValueError("Invalid YouTube URL. Couldn't find video ID.")
    video_id = video_id[0]
    return get_all_transcript(video_id)


from urllib.parse import urlparse, parse_qs

def get_youtube_transcript(youtube_url):
    video_id = parse_qs(urlparse(youtube_url).query).get("v")
    if not video_id or not isinstance(video_id[0], str):
        return "Error: Invalid YouTube URL. Couldn't extract video ID.", None

    return get_all_transcript(video_id[0])  # ✅ Pass the string only


from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

def get_all_transcript(video_id):
    """
    Fetches the best available transcript (manual or auto-generated) from a YouTube video.
    
    Returns:
    - transcript_text (str)
    - transcript_language (str), e.g., 'Hindi (HI)', 'English (EN)'
    """
    try:
        # Get available transcript list
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Pick manual transcript if available
        selected_transcript = None
        for t in transcript_list:
            if not t.is_generated:
                selected_transcript = t
                break

        # If no manual transcript, pick the first one (could be auto-generated)
        if selected_transcript is None:
            selected_transcript = list(transcript_list)[0]

        # Fetch entries safely and format
        transcript_entries = selected_transcript.fetch()
        transcript_text = " ".join([entry.text for entry in transcript_entries])
        transcript_language = f"{selected_transcript.language} ({selected_transcript.language_code.upper()})"

        return transcript_text, transcript_language

    except Exception as e:
        return f"Error fetching transcript: {e}", None




def detect_video_type(transcript, model):
    """Uses Gemini model to detect the genre of a video."""
    prompt = f"""
You are a helpful assistant. Classify the following YouTube video transcript into one of these categories ONLY: 
"educational", "motivational", "news", "product", or "general". 

Respond with only the single category name. Do not include any explanation.

Transcript:
{transcript[:12000]}

Category:
"""
    response = model.generate_content(prompt)
    return response.text.strip().lower()

def generate_prompt(transcript, question=None, video_type="general", task="chat", chat_history=None):
    """Creates a dynamic prompt for Gemini model based on context."""
    base_prompts = {
        "educational": "You are a helpful tutor. Engage in a multi-turn interactive Q&A session based on the transcript.",
        "motivational": "You are a motivational content explainer. Engage in a multi-turn conversation based on the transcript.",
        "product": "You are a product assistant helping users understand tech reviews or tutorials. Engage in a multi-turn conversation based on the transcript.",
        "news": "You are a factual news analyst. Engage in a multi-turn conversation based on the transcript.",
        "general": "You are a smart assistant that explains things clearly. Engage in a multi-turn conversation based on the transcript."
    }

    role = base_prompts.get(video_type.lower(), base_prompts["general"])

    prompt = f"""{role}
Based on the transcript below, answer the user's questions and engage in a conversation.

Transcript:
{transcript[:12000]}

"""
    if chat_history:
        for user_msg, bot_msg in chat_history:
            prompt += f"User: {user_msg}\nBot: {bot_msg}\n"
    prompt += f"User: {question}\nBot: "
    return prompt

def chat_with_transcript(model, transcript, video_type="general"):
    """Starts a command-line multi-turn chat based on video transcript."""
    chat_history = []
    while True:
        question = input("User: ")
        if question.lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye!")
            break
        prompt = generate_prompt(transcript, question, video_type, chat_history=chat_history)
        response = model.generate_content(prompt)
        answer = response.text
        print(f"User: {question}\nBot: {answer}")
        chat_history.append((question, answer))


LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "bn": "Bengali",
    # Add more as needed
}

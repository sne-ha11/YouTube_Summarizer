import streamlit as st
from google import genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import os
import re

# Load environment variables
load_dotenv()

API_KEY = os.getenv("Gemini_API_key")

client = genai.Client(api_key=API_KEY)



# Streamlit page configuration
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 AI YouTube Video Summarizer")

# User input
video_url = st.text_input(
    "Enter YouTube Video URL"
)


# Function to extract video ID
def get_video_id(url):

    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"

    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None


# Function to get transcript
def get_transcript(video_id):

    ytt_api = YouTubeTranscriptApi()

    fetched_transcript = ytt_api.fetch(video_id)

    text = " ".join(
        entry.text
        for entry in fetched_transcript
    )

    return text


# Generate summary when button is clicked
if st.button("Generate Summary"):

    video_id = get_video_id(video_url)

    if not video_id:
        st.error("Please enter a valid YouTube URL.")
        st.stop()

    # Show thumbnail
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"

    st.image(thumbnail_url)

    # Fetch transcript
    with st.spinner("Fetching transcript..."):

        transcript_text = get_transcript(video_id)

    # Prompt for Gemini
    prompt = f"""
You are an expert summarizer.

Convert this YouTube transcript into concise study notes.

Use:

# Headings
- Bullet points
- Important terms
- Key takeaways

Also provide a timestamped summary.

Format:

00:00 Introduction
03:25 Key Idea
08:10 Examples
15:30 Conclusion

Finally, generate 10 multiple-choice questions with answers.

Transcript:

{transcript_text}
"""

    # Gemini response
    with st.spinner("Generating summary..."):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

    st.subheader("Summary")

    st.write(response.text)
    
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from summary import summarize_text  # Import summarize_text from summary.py

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Set page configuration
st.set_page_config(page_title="GROQ Audio Transcription")

# Custom CSS for Streamlit theme-aware styling
st.markdown("""
    <style>
    /* Load Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Base styles */
    body {
        font-family: 'Inter', sans-serif;
    }
    .main {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stMarkdown p {
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* Card Styling */
    .card {
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 2rem;
        transition: transform 0.2s ease-in-out;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .stFileUploader:hover {
        border-color: #3b82f6;
    }
    /* Button Styling */
    .stButton > button {
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        transition: background-color 0.2s ease-in-out;
        width: 100%;
        max-width: 200px;
        margin: 1rem auto;
        display: block;
    }
    /* Audio Player */
    .stAudio {
        margin: 1rem 0;
        width: 100%;
    }
    /* Transcription and Summary */
    .transcription, .summary {
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
        font-size: 1rem;
        line-height: 1.6;
        text-align: justify; /* Justify text for transcription and summary */
    }
    h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    /* Spinner Styling */
    .stSpinner {
        text-align: center;
    }
    /* Error and Toast */
    .stToast {
        border-radius: 8px;
        padding: 1rem;
    }

    /* Light Theme (Streamlit) */
    .stThemeLight {
        background-color: #f4f7fa;
        color: #1f2a44;
    }
    .stThemeLight h1, .stThemeLight h3 {
        color: #1f2a44;
    }
    .stThemeLight .stMarkdown p {
        color: #64748b;
    }
    .stThemeLight .card {
        background: white;
    }
    .stThemeLight .stFileUploader {
        background: #ffffff;
        border-color: #e2e8f0;
    }
    .stThemeLight .stButton > button {
        background-color: #3b82f6;
        color: white;
    }
    .stThemeLight .stButton > button:hover {
        background-color: #2563eb;
    }
    .stThemeLight .transcription, .stThemeLight .summary {
        background: #f8fafc;
        color: #1f2a44;
    }
    .stThemeLight .stSpinner {
        color: #3b82f6;
    }
    .stThemeLight .stToast {
        background: #fef2f2;
        color: #dc2626;
    }

    /* Dark Theme (Streamlit) */
    .stThemeDark {
        background-color: #1f2a44;
        color: #e2e8f0;
    }
    .stThemeDark h1, .stThemeDark h3 {
        color: #e2e8f0;
    }
    .stThemeDark .stMarkdown p {
        color: #94a3b8;
    }
    .stThemeDark .card {
        background: #2d3748;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .stThemeDark .stFileUploader {
        background: #2d3748;
        border-color: #4b5563;
    }
    .stThemeDark .stFileUploader:hover {
        border-color: #60a5fa;
    }
    .stThemeDark .stButton > button {
        background-color: #60a5fa;
        color: #1f2a44;
    }
    .stThemeDark .stButton > button:hover {
        background-color: #3b82f6;
    }
    .stThemeDark .transcription, .stThemeDark .summary {
        background: #374151;
        color: #e2e8f0;
    }
    .stThemeDark .stSpinner {
        color: #60a5fa;
    }
    .stThemeDark .stToast {
        background: #7f1d1d;
        color: #f9fafb;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        .main {
            padding: 1rem;
        }
        .card {
            padding: 1rem;
        }
        .stButton > button {
            max-width: 100%;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Main container
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("📄 GROQ Audio Transcription")
    st.markdown(
        """
        Upload your audio file (WAV/MP3) to get a transcription and summary with ease.
        """,
        unsafe_allow_html=True
    )

    # Card for file uploader
    with st.container():
        uploaded_file = st.file_uploader(
            "Choose an audio file", type=["wav", "mp3", "m4a", "flac"], label_visibility="collapsed"
        )

    # Display uploaded file and audio player
    if uploaded_file is not None:
        with st.container():
            temp_path = os.path.join("temp_audio" + os.path.splitext(uploaded_file.name)[1])
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.audio(uploaded_file, format="audio/" + uploaded_file.type.split("/")[-1])
            st.markdown(f"<p><strong>File:</strong> {uploaded_file.name}</p>", unsafe_allow_html=True)

            # Transcribe button
            if st.button("Transcribe"):
                with st.spinner("Processing..."):
                    try:
                        with open(temp_path, "rb") as audio:
                            transcription = client.audio.transcriptions.create(
                                file=audio,
                                model="whisper-large-v3-turbo",
                                prompt="",
                                response_format="verbose_json",
                                timestamp_granularities=["word", "segment"],
                                language="id",
                                temperature=0.0
                            )

                        full_text = " ".join(seg["text"] for seg in transcription.segments if "text" in seg)

                        # Transcription card
                        with st.container():
                            st.subheader("Transcription Text:")
                            st.markdown(f'<div class="transcription">{full_text}</div>', unsafe_allow_html=True)

                        # Summary
                        with st.spinner("Summarizing transcription..."):
                            summary = summarize_text(full_text)

                        # Summary card
                        with st.container():
                            st.subheader("Text Summary:")
                            st.markdown(f'<div class="summary">{summary}</div>', unsafe_allow_html=True)

                    except Exception as e:
                        error_message = str(e)
                        st.toast(f"Error: {error_message}", icon="⚠️")
                        st.error("Transcription or summarization failed. Please try again.")
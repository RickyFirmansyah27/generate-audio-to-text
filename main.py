import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

st.set_page_config(page_title="GROQ Audio Transcription", layout="centered")
st.title("📄 GROQ Audio Transcription")

st.write(
    """
    Unggah file audio Anda (WAV/MP3) dan dapatkan hasil transkripsi beserta timestamp-nya.
    """
)

uploaded_file = st.file_uploader(
    "Pilih file audio", type=["wav", "mp3", "m4a", "flac"]
)

if uploaded_file is not None:

    temp_path = os.path.join("temp_audio" + os.path.splitext(uploaded_file.name)[1])
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.audio(uploaded_file, format="audio/" + uploaded_file.type.split("/")[-1])
    st.write(f"**File:** {uploaded_file.name}")


    if st.button("Transcribe"):
        with st.spinner("Memproses..."):
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
                st.subheader("Teks Transkripsi:")
                st.write(full_text)

            except Exception as e:
                # Tangkap pesan error dari exception
                error_message = str(e)
                st.toast(f"Error: {error_message}", icon="⚠️")
                st.error("Transkripsi gagal. Silakan coba lagi.")

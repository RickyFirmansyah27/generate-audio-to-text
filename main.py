import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

# Ambil API key dari lingkungan
groq_api_key = os.getenv("GROQ_API_KEY")

# Inisialisasi klien GROQ dengan API key yang diambil dari env
client = Groq(api_key=groq_api_key)

st.set_page_config(page_title="GROQ Audio Transcription", layout="centered")
st.title("📄 GROQ Audio Transcription")

st.write(
    """
    Unggah file audio Anda (WAV/MP3) dan dapatkan hasil transkripsi beserta timestamp-nya.
    """
)

# File uploader
uploaded_file = st.file_uploader(
    "Pilih file audio", type=["wav", "mp3", "m4a", "flac"]
)

if uploaded_file is not None:
    # Simpan sementara
    temp_path = os.path.join("temp_audio" + os.path.splitext(uploaded_file.name)[1])
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.audio(uploaded_file, format="audio/" + uploaded_file.type.split("/")[-1])
    st.write(f"**File:** {uploaded_file.name}")

    # Tombol untuk mulai transkripsi
    if st.button("Transcribe"):
        with st.spinner("Memproses..."):
            with open(temp_path, "rb") as audio:
                transcription = client.audio.transcriptions.create(
                    file=audio,
                    model="whisper-large-v3-turbo",
                    prompt="",
                    response_format="verbose_json",
                    timestamp_granularities=["word", "segment"],
                    language="en",
                    temperature=0.0
                )
    
        try:
            full_text = " ".join(seg["text"] for seg in transcription.segments if "text" in seg)
        except KeyError:
            st.error("Unexpected response format. Please check the API response.")
            full_text = ""
        st.subheader("Teks Transkripsi:")
        st.write(full_text)

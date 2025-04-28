import os
import json
import streamlit as st
import subprocess
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

def convert_to_flac(input_file: str, output_file: str):
    # Menggunakan ffmpeg untuk mengonversi file audio ke format FLAC dengan pengaturan bitrate dan sample rate yang lebih rendah
    subprocess.run([
        'ffmpeg', '-i', input_file, '-ar', '16000', '-ac', '1', '-map', '0:a', '-c:a', 'flac', output_file
    ])

if uploaded_file is not None:
    # Simpan sementara
    temp_path = os.path.join("temp_audio" + os.path.splitext(uploaded_file.name)[1])
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.audio(uploaded_file, format="audio/" + uploaded_file.type.split("/")[-1])
    st.write(f"**File:** {uploaded_file.name}")

    # Cek ukuran file dan konversi jika lebih besar dari 40 MB
    if os.path.getsize(temp_path) > 40 * 1024 * 1024:  # 40 MB dalam byte
        st.write("File terlalu besar, mengonversi ke FLAC...")
        flac_file = temp_path.replace(os.path.splitext(uploaded_file.name)[1], ".flac")
        convert_to_flac(temp_path, flac_file)
        temp_path = flac_file  # Ganti file yang akan diproses dengan file FLAC yang baru

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

import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="GROQ Audio Transcription", layout="wide")

with st.sidebar:
    st.title("🔑 API Key Settings")
    

    api_key_input = st.text_input(
        "Masukkan GROQ API Key Anda:",
        type="password",
        help="Dapatkan API key dari https://console.groq.com/keys"
    )
    

    groq_api_key = api_key_input or os.getenv("GROQ_API_KEY")
    

    if api_key_input and st.button("Simpan API Key ke .env"):
        try:
            with open(".env", "w") as f:
                f.write(f"GROQ_API_KEY={api_key_input}")
            st.success("API Key berhasil disimpan ke file .env!")
        except Exception as e:
            st.error(f"Gagal menyimpan API Key: {str(e)}")
    
    st.markdown("---")
    
    st.markdown("Aplikasi ini menggunakan Groq API untuk transkripsi audio ke teks.")

st.title("📄 GROQ Audio Transcription")

st.write(
    """
    Unggah file audio Anda (WAV/MP3) dan dapatkan hasil transkripsi beserta timestamp-nya.
    """
)

if not groq_api_key:
    st.warning("⚠️ Silakan masukkan API key GROQ di sidebar untuk menggunakan aplikasi ini.")

uploaded_file = st.file_uploader(
    "Pilih file audio", type=["wav", "mp3", "m4a", "flac"]
)

if uploaded_file is not None:

    os.makedirs("temp", exist_ok=True)
    

    temp_path = os.path.join("temp", "temp_audio" + os.path.splitext(uploaded_file.name)[1])
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


    st.audio(uploaded_file, format="audio/" + uploaded_file.type.split("/")[-1])
    st.write(f"**File:** {uploaded_file.name}")


    if st.button("Transcribe"):
        if not groq_api_key:
            st.error("API Key diperlukan untuk transkripsi. Silakan masukkan API Key di sidebar.")
        else:
            with st.spinner("Memproses..."):
                try:

                    client = Groq(api_key=groq_api_key)
                    
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
                    

                    with st.expander("Lihat Detail Segmen dan Timestamp"):
                        for i, segment in enumerate(transcription.segments):
                            if "text" in segment and "start" in segment and "end" in segment:
                                st.markdown(f"**Segmen {i+1}:** {segment['text']}")
                                st.markdown(f"Waktu: {segment['start']:.2f}s - {segment['end']:.2f}s")
                                st.markdown("---")
                    

                    st.download_button(
                        label="Download Transkripsi (JSON)",
                        data=json.dumps(transcription.model_dump(), indent=2),
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcript.json",
                        mime="application/json"
                    )
                    

                    st.download_button(
                        label="Download Transkripsi (Text)",
                        data=full_text,
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcript.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:

                    error_message = str(e)
                    st.toast(f"Error: {error_message}", icon="⚠️")
                    st.error("Transkripsi gagal. Silakan coba lagi.")

if st.button("Bersihkan File Sementara"):
    try:
        import shutil
        shutil.rmtree("temp", ignore_errors=True)
        os.makedirs("temp", exist_ok=True)
        st.success("File sementara berhasil dibersihkan!")
    except Exception as e:
        st.error(f"Gagal membersihkan file: {str(e)}")

st.markdown("---")
st.markdown("Dibuat dengan ❤️ menggunakan Streamlit dan Groq API")
# summary.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def summarize_text(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Anda adalah asisten yang membantu merangkum teks dalam bahasa Indonesia."
            },
            {
                "role": "user",
                "content": f"Tolong rangkum teks berikut dengan penjelasan secara scientific dan jelaskan setiap kalimat:\n\n{text}"
            }
        ],
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def translate_audio(file_path):
    url = "https://api.groq.com/openai/v1/audio/translations"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    with open(file_path, 'rb') as f:
        files = {
            'file': (file_path, f),
            'model': (None, 'whisper-large-v3')
        }

        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json()['text']

def llama_query(prompt, model="llama-3.3-70b-versatile"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def translate_text(text):
    prompt = f"""You are a translator AI. Translate the user input: "{text}" to English. Return translation only."""
    return llama_query(prompt)
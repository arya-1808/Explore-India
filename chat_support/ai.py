import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_ai_response(message):
    prompt = f"""
You are Explore India AI Travel Assistant.

Answer only questions related to tourism in India.
Be polite and helpful.

User: {message}
"""

    response = model.generate_content(prompt)
    return response.text
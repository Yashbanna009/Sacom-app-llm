import google.generativeai as genai
from backend.config import settings

class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")

    def get_response(self, system_prompt: str, user_message: str) -> str:
        try:
            prompt = f"{system_prompt}\nUser: {user_message}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Google Gemini API Error: {e}")
            return "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later." 
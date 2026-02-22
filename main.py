import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME")

client = genai.Client(api_key=API_KEY)

modelo = client.models.generate_content(
    model_name=MODEL_NAME,
    contents="""
        
    """
)

print(f"Api key from gemini ai {API_KEY}")
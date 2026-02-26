import os
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAEB4xJEtmo867KGSOjezKMlqK6DsXTnok")
MODEL_NAME = "gemini-3-flash-preview"

client = genai.Client(api_key=API_KEY)

import os
import sys
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"

if not API_KEY:
    print("エラー: GEMINI_API_KEY 環境変数が設定されていません。", file=sys.stderr)
    print("  export GEMINI_API_KEY='your-api-key'", file=sys.stderr)
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

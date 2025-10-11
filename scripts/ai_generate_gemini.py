import os
from google import genai
from google.genai.types import HttpOptions, Content

# 初始化 Gemini 客戶端
MODEL = 'gemini-2.0-flash'
def init_gemini_client():
    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"], 
        http_options=HttpOptions(api_version="v1")
    )
    return client
def generate_text(prompt: str) -> str:
    """
    使用 AI 生成文本
    """
    client = init_gemini_client()
    response = client.models.generate_content(contents=prompt, model=MODEL)
    return response.text

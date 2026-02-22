import os
import random
from dotenv import load_dotenv

load_dotenv()

def get_embedding(text: str):
    """
    تولید embedding برای متن
    اگر OPENAI_API_KEY موجود باشد از OpenAI استفاده می‌کند
    در غیر این صورت شبیه‌سازی می‌کند
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key and api_key != "your_openai_api_key_here":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"[Embedding] Error using OpenAI: {e}, falling back to random")
    
    # Fallback: شبیه‌سازی
    return [random.random() for _ in range(1536)]
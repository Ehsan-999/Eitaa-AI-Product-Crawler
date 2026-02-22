import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """
Extract structured product data from this Persian caption.

Return JSON with this format:
{
  "sizes": [],
  "colors": [],
  "material": ""
}

Caption:
{caption}
"""

def extract_entities(caption: str):
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "sizes": [],
            "colors": [],
            "material": None
        }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PROMPT.format(caption=caption)}],
        temperature=0
    )

    import json
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {
            "sizes": [],
            "colors": [],
            "material": None
        }
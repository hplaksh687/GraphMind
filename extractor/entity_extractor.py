import json
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def extract_entities(text: str, source: str) -> list:
    prompt = f"""You are a knowledge extraction AI.
From the text below, extract all important entities (people, organizations, concepts, technologies, places, events).
Return ONLY a valid JSON array like this:
[
  {{"name": "Entity Name", "type": "Person/Organization/Concept/Technology/Place/Event"}}
]
No explanation. No markdown. Just the JSON array.
TEXT:
{text[:4000]}"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"Entity extraction error: {e}")
        return []

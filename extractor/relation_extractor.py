import json
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def extract_relations(text: str, entities: list) -> list:
    entity_names = [e["name"] for e in entities]
    prompt = f"""You are a knowledge graph AI.
Given these entities: {entity_names}
From the text below, extract relationships between these entities.
Return ONLY a valid JSON array like this:
[
  {{"from": "Entity A", "relation": "RELATIONSHIP", "to": "Entity B"}}
]
Rules:
- Only use entities from the list above
- Keep relation short (1-4 words)
- No explanation. No markdown. Just JSON array.
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
        print(f"Relation extraction error: {e}")
        return []
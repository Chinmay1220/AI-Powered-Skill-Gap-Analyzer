from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_EMBED_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_text(text: str) -> list[float]:
    # Keep embeddings input reasonable
    text = text.strip()
    resp = client.embeddings.create(
        model=OPENAI_EMBED_MODEL,
        input=text
    )
    return resp.data[0].embedding

def chat_json(system_prompt: str, user_prompt: str) -> str:
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content

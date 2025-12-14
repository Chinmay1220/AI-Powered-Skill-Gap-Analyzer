import json
from backend.openai_client import embed_text
from backend.pinecone_client import ensure_index, get_index

def main():
    # Use one embedding to get dimension
    dim = len(embed_text("dimension check"))
    ensure_index(dim)
    index = get_index()

    vectors = []
    with open("data/seed_docs.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            text = obj["text"]
            emb = embed_text(text)

            metadata = {
                "type": obj.get("type"),
                "role": obj.get("role"),
                "level": obj.get("level"),
                "skill": obj.get("skill"),
                "text": text
            }
            metadata = {k: v for k, v in metadata.items() if v is not None}
            vectors.append((obj["id"], emb, metadata))

    # Upsert in batches
    B = 50
    for i in range(0, len(vectors), B):
        batch = vectors[i:i+B]
        index.upsert(vectors=batch)
        print(f"Upserted {i+len(batch)}/{len(vectors)}")

if __name__ == "__main__":
    main()

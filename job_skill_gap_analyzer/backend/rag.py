from typing import List, Dict, Any
from .openai_client import embed_text
from .pinecone_client import get_index
from .config import MAX_CONTEXT_DOCS

def retrieve_context(query: str, top_k: int = None) -> List[Dict[str, Any]]:
    if top_k is None:
        top_k = MAX_CONTEXT_DOCS

    q_emb = embed_text(query)
    index = get_index()

    res = index.query(
        vector=q_emb,
        top_k=top_k,
        include_metadata=True
    )

    docs = []
    for m in res.get("matches", []):
        md = m.get("metadata", {}) or {}
        docs.append({
            "score": m.get("score"),
            "id": m.get("id"),
            "type": md.get("type"),
            "role": md.get("role"),
            "level": md.get("level"),
            "skill": md.get("skill"),
            "text": md.get("text", "")
        })
    return docs

def format_context(docs: List[Dict[str, Any]]) -> str:
    lines = []
    for d in docs:
        header_parts = []
        if d.get("type"): header_parts.append(f"type={d['type']}")
        if d.get("role"): header_parts.append(f"role={d['role']}")
        if d.get("level"): header_parts.append(f"level={d['level']}")
        if d.get("skill"): header_parts.append(f"skill={d['skill']}")
        header = ", ".join(header_parts) if header_parts else "doc"
        lines.append(f"- ({header}) {d.get('text','')}")
    return "\n".join(lines)

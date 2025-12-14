from pinecone import Pinecone, ServerlessSpec
from .config import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_CLOUD, PINECONE_REGION

pc = Pinecone(api_key=PINECONE_API_KEY)

def ensure_index(dimension: int):
    existing = [idx["name"] for idx in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
        )

def get_index():
    return pc.Index(PINECONE_INDEX_NAME)

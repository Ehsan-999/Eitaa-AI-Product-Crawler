import numpy as np
from app.db.database import SessionLocal
from app.db.models import Product
from app.ai.embedding import get_embedding

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_products(query: str, top_k=10):
    db = SessionLocal()
    query_embedding = get_embedding(query)

    products = db.query(Product).all()
    scored = []

    for p in products:
        if not p.embedding:
            continue
        score = cosine(query_embedding, p.embedding)
        scored.append((score, p))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [p for _, p in scored[:top_k]]
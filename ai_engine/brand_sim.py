"""
brand_sim.py
- brand_similarity(host) -> best_brand + similarity
Uses sentence-transformers embeddings if available; fallback to token Jaccard.
"""

import re
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    EMB_MODEL = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    EMB_AVAILABLE = True
except Exception:
    EMB_MODEL = None
    EMB_AVAILABLE = False

# Curated small brand list. Expand to 200+ for final build.
BRAND_LIST = [
    "google.com","amazon.in","amazon.com","paytm.com","sbi.co.in","icici.com","axisbank.com",
    "flipkart.com","airtel.in","gmail.com","facebook.com","instagram.com","phonepe.com",
    "hdfcbank.com","paytm.in","uidai.gov.in"
]

if EMB_AVAILABLE:
    brand_embs = {b: EMB_MODEL.encode(b) for b in BRAND_LIST}
else:
    brand_embs = {}

def token_jaccard(a: str, b: str) -> float:
    at = set([t for t in re.split(r'[\W_]+', a.lower()) if t])
    bt = set([t for t in re.split(r'[\W_]+', b.lower()) if t])
    if not at or not bt:
        return 0.0
    return len(at & bt) / len(at | bt)

def brand_similarity(host: str) -> dict:
    """
    Returns best matching brand and similarity score (0-1).
    If embedding available, uses embedding cosine similarity; else token jaccard.
    """
    if not host:
        return {"best_brand": None, "sim": 0.0}
    if EMB_AVAILABLE:
        h_emb = EMB_MODEL.encode(host)
        best, best_score = None, -1.0
        for b, emb in brand_embs.items():
            sim = float(np.dot(h_emb, emb) / (np.linalg.norm(h_emb) * np.linalg.norm(emb)))
            if sim > best_score:
                best, best_score = b, sim
        return {"best_brand": best, "sim": float(best_score)}
    else:
        best, best_score = None, -1.0
        for b in BRAND_LIST:
            sim = token_jaccard(host, b)
            if sim > best_score:
                best, best_score = b, sim
        return {"best_brand": best, "sim": float(best_score)}

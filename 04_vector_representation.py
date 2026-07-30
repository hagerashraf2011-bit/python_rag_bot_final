from importlib import import_module
import json
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

preprocessing = import_module("02_preprocessing")
chunks = import_module("03_chunking").build_chunks()

# ALPHA is chosen automatically by evaluation/evaluate_retrieval.py, which
# sweeps alpha from 0.0 (pure BM25) to 1.0 (pure embeddings) against
# ground-truth queries and writes the best-scoring value to
# data/best_config.json. If that file doesn't exist yet (evaluation has
# never been run), fall back to 0.6 — the value that performed best in the
# original lab experiments (Lab7/Lab8) and is a reasonable default.
DEFAULT_ALPHA = 0.6
BEST_CONFIG_PATH = Path(__file__).resolve().parent / "data" / "best_config.json"

try:
    ALPHA = json.loads(BEST_CONFIG_PATH.read_text(encoding="utf-8"))["alpha"]
    print(f"[04_vector_representation] Using evaluated ALPHA={ALPHA} from {BEST_CONFIG_PATH.name}")
except (FileNotFoundError, KeyError, json.JSONDecodeError):
    ALPHA = DEFAULT_ALPHA
    print(f"[04_vector_representation] No evaluation results found, using default ALPHA={ALPHA}. "
          f"Run: python evaluation/evaluate_retrieval.py")

MODEL_NAME = "all-MiniLM-L6-v2"

tokenized_chunks = [chunk["search_text"].split() for chunk in chunks]
bm25 = BM25Okapi(tokenized_chunks)

model = SentenceTransformer(MODEL_NAME)
chunk_embeddings = model.encode(
    [chunk["search_text"] for chunk in chunks],
    convert_to_numpy=True,
    normalize_embeddings=True,
)


def min_max_normalize(scores):
    scores = np.array(scores, dtype=float)
    if scores.max() == scores.min():
        return np.zeros_like(scores)
    return (scores - scores.min()) / (scores.max() - scores.min())


def hybrid_search(query, k=4):
    clean_query = preprocessing.preprocess_text(query)

    bm25_scores = bm25.get_scores(clean_query.split())
    query_embedding = model.encode(
        [clean_query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    embedding_scores = cosine_similarity(query_embedding, chunk_embeddings).flatten()

    hybrid_scores = ((1 - ALPHA) * min_max_normalize(bm25_scores)) + (
        ALPHA * min_max_normalize(embedding_scores)
    )

    ranking = np.argsort(hybrid_scores)[::-1][:k]
    return [
        {**chunks[index], "score": hybrid_scores[index]}
        for index in ranking
    ]

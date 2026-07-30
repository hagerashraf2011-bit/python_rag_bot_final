"""
Evaluates retrieval quality on the 61-topic knowledge base, the same way
Lab6/Lab7/Lab8 evaluated TF-IDF vs BM25 vs embeddings vs hybrid — but run
here against this project's actual documents and ground-truth queries.

What it does:
1. Builds a TF-IDF index, a BM25 index, and a sentence-embedding index over
   the project's chunks (03_chunking.py).
2. Scores every ground-truth query (evaluation/ground_truth.py) against
   each retriever using Precision@3, Recall@3, Hit Rate@3, and Mean
   Reciprocal Rank — identical metrics to the ones used in the labs.
3. Sweeps the hybrid weight (alpha) from 0.0 (pure BM25) to 1.0
   (pure embeddings) in steps of 0.1, since the hybrid formula already
   covers BM25-only and embeddings-only as its two edge cases.
4. Picks the single best-performing alpha automatically (ranked by mean
   reciprocal rank, tie-broken by Hit Rate@3) and writes it to
   data/best_config.json.
5. 04_vector_representation.py reads that file on import, so the live app
   automatically uses whichever configuration scored best here — no manual
   editing needed.

Run it once after adding/editing topics in 01_documents.py:

    python evaluation/evaluate_retrieval.py
"""
import re
import sys
import json
from importlib import import_module
from pathlib import Path

import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

chunks = import_module("03_chunking").build_chunks()
ground_truth = import_module("ground_truth").ground_truth

pd.set_option("display.max_colwidth", 120)
pd.set_option("display.width", 160)

MODEL_NAME = "all-MiniLM-L6-v2"
K = 3
ALPHA_SWEEP = [round(a, 1) for a in np.arange(0.0, 1.01, 0.1)]


# --------------------------------------------------------------- metrics --
def precision_at_k(retrieved_ids, relevant_ids, k):
    hits = set(retrieved_ids[:k]).intersection(set(relevant_ids))
    return len(hits) / k


def recall_at_k(retrieved_ids, relevant_ids, k):
    hits = set(retrieved_ids[:k]).intersection(set(relevant_ids))
    return len(hits) / len(relevant_ids)


def hit_rate_at_k(retrieved_ids, relevant_ids, k):
    hits = set(retrieved_ids[:k]).intersection(set(relevant_ids))
    return int(len(hits) > 0)


def reciprocal_rank(retrieved_ids, relevant_ids):
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1 / rank
    return 0.0


def evaluate_retriever(name, retrieval_function, ground_truth, k=K):
    rows = []
    for item in ground_truth:
        query, relevant_ids = item["query"], [item["relevant_document_id"]]
        results = retrieval_function(query, k=max(k, 5))
        retrieved_ids = results["document_id"].tolist()
        rows.append({
            "retriever": name,
            "query": query,
            f"precision@{k}": precision_at_k(retrieved_ids, relevant_ids, k),
            f"recall@{k}": recall_at_k(retrieved_ids, relevant_ids, k),
            f"hit_rate@{k}": hit_rate_at_k(retrieved_ids, relevant_ids, k),
            "reciprocal_rank": reciprocal_rank(retrieved_ids, relevant_ids),
        })
    return pd.DataFrame(rows)


# ------------------------------------------------------------- indexing --
def normalize_lexical_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def min_max_normalize(scores):
    scores = np.array(scores, dtype=float)
    if scores.max() == scores.min():
        return np.zeros_like(scores)
    return (scores - scores.min()) / (scores.max() - scores.min())


print(f"Building indices over {len(chunks)} chunks ...")

search_texts = [c["search_text"] for c in chunks]
doc_ids = [c["document_id"] for c in chunks]
titles = [c["title"] for c in chunks]

tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_matrix = tfidf_vectorizer.fit_transform([normalize_lexical_text(t) for t in search_texts])

tokenized_chunks = [normalize_lexical_text(t).split() for t in search_texts]
bm25 = BM25Okapi(tokenized_chunks)

model = SentenceTransformer(MODEL_NAME)
chunk_embeddings = model.encode(search_texts, convert_to_numpy=True, normalize_embeddings=True)

print("Indices ready.\n")


# --------------------------------------------------------------- search --
def retrieve_top_k_tfidf(query, k=3):
    query_vector = tfidf_vectorizer.transform([normalize_lexical_text(query)])
    scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    ranking = np.argsort(scores)[::-1][:k]
    return pd.DataFrame({"document_id": [doc_ids[i] for i in ranking], "title": [titles[i] for i in ranking], "score": scores[ranking]})


def retrieve_top_k_bm25(query, k=3):
    scores = bm25.get_scores(normalize_lexical_text(query).split())
    ranking = np.argsort(scores)[::-1][:k]
    return pd.DataFrame({"document_id": [doc_ids[i] for i in ranking], "title": [titles[i] for i in ranking], "score": scores[ranking]})


def retrieve_top_k_semantic(query, k=3):
    query_embedding = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    scores = cosine_similarity(query_embedding, chunk_embeddings).flatten()
    ranking = np.argsort(scores)[::-1][:k]
    return pd.DataFrame({"document_id": [doc_ids[i] for i in ranking], "title": [titles[i] for i in ranking], "score": scores[ranking]})


def retrieve_top_k_hybrid(query, alpha, k=3):
    lexical_query_vector = tfidf_vectorizer.transform([normalize_lexical_text(query)])
    bm25_scores = bm25.get_scores(normalize_lexical_text(query).split())
    query_embedding = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    semantic_scores = cosine_similarity(query_embedding, chunk_embeddings).flatten()

    combined = (1 - alpha) * min_max_normalize(bm25_scores) + alpha * min_max_normalize(semantic_scores)
    ranking = np.argsort(combined)[::-1][:k]
    return pd.DataFrame({"document_id": [doc_ids[i] for i in ranking], "title": [titles[i] for i in ranking], "score": combined[ranking]})


# ---------------------------------------------------------------- run --
print("Evaluating TF-IDF, BM25, embeddings-only baselines ...")
tfidf_eval = evaluate_retriever("TF-IDF", lambda q, k: retrieve_top_k_tfidf(q, k), ground_truth)
bm25_eval = evaluate_retriever("BM25 (alpha=0.0)", lambda q, k: retrieve_top_k_hybrid(q, 0.0, k), ground_truth)
semantic_eval = evaluate_retriever("Embeddings (alpha=1.0)", lambda q, k: retrieve_top_k_hybrid(q, 1.0, k), ground_truth)

print("Sweeping hybrid alpha from 0.0 to 1.0 ...")
hybrid_evals = []
for alpha in ALPHA_SWEEP:
    if alpha in (0.0, 1.0):
        continue  # already covered by the BM25-only / embeddings-only rows above
    ev = evaluate_retriever(f"Hybrid alpha={alpha}", lambda q, k, a=alpha: retrieve_top_k_hybrid(q, a, k), ground_truth)
    hybrid_evals.append(ev)

all_eval = pd.concat([tfidf_eval, bm25_eval, semantic_eval] + hybrid_evals, ignore_index=True)

summary = (
    all_eval.groupby("retriever")[[f"precision@{K}", f"recall@{K}", f"hit_rate@{K}", "reciprocal_rank"]]
    .mean()
    .sort_values(by=["reciprocal_rank", f"hit_rate@{K}"], ascending=False)
)

print("\n=== Retrieval comparison (mean over all ground-truth queries) ===")
print(summary.round(3).to_string())

# --------------------------------------------------- pick the winner --
# TF-IDF is reported for reference only (same baseline used in the labs);
# the production hybrid_search() only ever mixes BM25 and embeddings, so
# the automatic pick is restricted to that same alpha family (0.0-1.0,
# where 0.0 = pure BM25 and 1.0 = pure embeddings).
hybrid_candidates = summary[summary.index != "TF-IDF"]
best_name = hybrid_candidates.index[0]
best_row = hybrid_candidates.iloc[0]

if best_name.startswith("BM25"):
    best_alpha = 0.0
elif best_name.startswith("Embeddings"):
    best_alpha = 1.0
else:
    best_alpha = float(best_name.split("alpha=")[1])

print(f"\nBest configuration: {best_name}")
print(f"  -> alpha = {best_alpha}")
print(f"  -> mean reciprocal rank = {best_row['reciprocal_rank']:.3f}")
print(f"  -> hit_rate@{K} = {best_row[f'hit_rate@{K}']:.3f}")

# ---------------------------------------------------------------- save --
data_dir = PROJECT_ROOT / "data"
data_dir.mkdir(exist_ok=True)

best_config = {
    "alpha": best_alpha,
    "selected_from": best_name,
    "mean_reciprocal_rank": round(float(best_row["reciprocal_rank"]), 4),
    f"hit_rate@{K}": round(float(best_row[f"hit_rate@{K}"]), 4),
    "num_ground_truth_queries": len(ground_truth),
}
(data_dir / "best_config.json").write_text(json.dumps(best_config, indent=2), encoding="utf-8")
print(f"\nWrote {data_dir / 'best_config.json'} — 04_vector_representation.py will use this alpha automatically.")

report_lines = [
    "# Retrieval Evaluation Results",
    "",
    f"Evaluated on {len(chunks)} chunks ({len(chunks)} topics) using {len(ground_truth)} "
    "naturally-phrased ground-truth queries (not copied from topic titles), "
    "following the same Precision@3 / Recall@3 / Hit Rate@3 / Mean Reciprocal "
    "Rank methodology used in Lab6, Lab7, and Lab8.",
    "",
    "## Comparison table",
    "",
    summary.round(3).to_markdown(),
    "",
    f"## Automatically selected configuration",
    "",
    f"**Winner: `{best_name}`** (alpha = {best_alpha}), chosen automatically by "
    "highest mean reciprocal rank, tie-broken by Hit Rate@3.",
    "",
    "This value is written to `data/best_config.json` and read by "
    "`04_vector_representation.py` at import time, so the live retrieval "
    "pipeline always uses whichever configuration this evaluation found best "
    "— re-run this script after changing the knowledge base and the app "
    "picks up the new value with no manual editing.",
]
(Path(__file__).resolve().parent / "evaluation_results.md").write_text(
    "\n".join(report_lines), encoding="utf-8"
)
print(f"Wrote {Path(__file__).resolve().parent / 'evaluation_results.md'}")
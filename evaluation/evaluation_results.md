# Retrieval Evaluation Results

Evaluated on 83 chunks (61 topics) using 166 naturally-phrased ground-truth queries (not copied from topic titles), following the same Precision@3 / Recall@3 / Hit Rate@3 / Mean Reciprocal Rank methodology used in Lab6, Lab7, and Lab8.

## Comparison table

| retriever              |   precision@3 |   recall@3 |   hit_rate@3 |   reciprocal_rank |
|:-----------------------|--------------:|-----------:|-------------:|------------------:|
| Hybrid alpha=0.6       |         0.313 |      0.94  |        0.94  |             0.869 |
| Hybrid alpha=0.7       |         0.311 |      0.934 |        0.934 |             0.865 |
| Hybrid alpha=0.8       |         0.311 |      0.934 |        0.934 |             0.855 |
| Hybrid alpha=0.5       |         0.311 |      0.934 |        0.934 |             0.853 |
| Hybrid alpha=0.4       |         0.305 |      0.916 |        0.916 |             0.838 |
| Hybrid alpha=0.9       |         0.311 |      0.934 |        0.934 |             0.836 |
| Hybrid alpha=0.3       |         0.299 |      0.898 |        0.898 |             0.812 |
| Embeddings (alpha=1.0) |         0.301 |      0.904 |        0.904 |             0.798 |
| Hybrid alpha=0.2       |         0.289 |      0.867 |        0.867 |             0.794 |
| Hybrid alpha=0.1       |         0.287 |      0.861 |        0.861 |             0.772 |
| BM25 (alpha=0.0)       |         0.283 |      0.849 |        0.849 |             0.758 |
| TF-IDF                 |         0.275 |      0.825 |        0.825 |             0.721 |

## Automatically selected configuration

**Winner: `Hybrid alpha=0.6`** (alpha = 0.6), chosen automatically by highest mean reciprocal rank, tie-broken by Hit Rate@3.

This value is written to `data/best_config.json` and read by `04_vector_representation.py` at import time, so the live retrieval pipeline always uses whichever configuration this evaluation found best — re-run this script after changing the knowledge base and the app picks up the new value with no manual editing.
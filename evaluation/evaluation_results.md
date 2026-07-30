# Retrieval Evaluation Results

Evaluated on 83 chunks (83 topics) using 166 naturally-phrased ground-truth queries (not copied from topic titles), following the same Precision@3 / Recall@3 / Hit Rate@3 / Mean Reciprocal Rank methodology used in Lab6, Lab7, and Lab8.

## Comparison table

| retriever              |   precision@3 |   recall@3 |   hit_rate@3 |   reciprocal_rank |
|:-----------------------|--------------:|-----------:|-------------:|------------------:|
| Hybrid alpha=0.9       |         0.265 |      0.795 |        0.795 |             0.682 |
| Hybrid alpha=0.8       |         0.269 |      0.807 |        0.807 |             0.681 |
| Hybrid alpha=0.7       |         0.259 |      0.777 |        0.777 |             0.666 |
| Embeddings (alpha=1.0) |         0.261 |      0.783 |        0.783 |             0.664 |
| Hybrid alpha=0.6       |         0.237 |      0.711 |        0.711 |             0.644 |
| Hybrid alpha=0.5       |         0.223 |      0.669 |        0.669 |             0.605 |
| Hybrid alpha=0.4       |         0.213 |      0.639 |        0.639 |             0.558 |
| Hybrid alpha=0.3       |         0.207 |      0.62  |        0.62  |             0.524 |
| Hybrid alpha=0.2       |         0.199 |      0.596 |        0.596 |             0.511 |
| TF-IDF                 |         0.181 |      0.542 |        0.542 |             0.485 |
| Hybrid alpha=0.1       |         0.185 |      0.554 |        0.554 |             0.481 |
| BM25 (alpha=0.0)       |         0.175 |      0.524 |        0.524 |             0.46  |

## Automatically selected configuration

**Winner: `Hybrid alpha=0.9`** (alpha = 0.9), chosen automatically by highest mean reciprocal rank, tie-broken by Hit Rate@3.

This value is written to `data/best_config.json` and read by `04_vector_representation.py` at import time, so the live retrieval pipeline always uses whichever configuration this evaluation found best — re-run this script after changing the knowledge base and the app picks up the new value with no manual editing.
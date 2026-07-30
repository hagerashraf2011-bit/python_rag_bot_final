from importlib import import_module

hybrid_search = import_module("04_vector_representation").hybrid_search

# Chunks scoring below this are treated as "not relevant enough" rather than
# forced into the answer. Kept low and permissive on purpose: short, common
# questions (e.g. "how to print") produce a low absolute hybrid score even
# when the retrieved chunk is clearly correct, so an aggressive threshold
# ends up rejecting valid questions. Tune this value against real test
# questions before raising it.
MIN_RELEVANCE_SCORE = 0.08


def build_context(question, k=6, max_sources=3, min_score=MIN_RELEVANCE_SCORE):
    rows = hybrid_search(question, k=k)
    rows = sorted(rows, key=lambda row: (row["is_current"], row["score"]), reverse=True)

    retrieved_ids = {row["document_id"] for row in rows if row["score"] >= min_score}

    selected = []
    seen_documents = set()

    for row in rows:
        if row["score"] < min_score:
            continue
        if row["document_id"] in seen_documents:
            continue

        # Conflict resolution: if this row is outdated AND the current doc it
        # was replaced by was *also* retrieved for this question, drop the
        # outdated one — the current version alone is the better answer.
        # If no current replacement showed up, keep the outdated row so the
        # bot can still answer (and clearly label it as outdated below).
        if not row["is_current"] and row.get("replaces") in retrieved_ids:
            continue

        selected.append(row)
        seen_documents.add(row["document_id"])
        if len(selected) == max_sources:
            break

    context = ""
    for source_number, row in enumerate(selected, start=1):
        status = "CURRENT" if row["is_current"] else "OUTDATED — do not recommend this, prefer current practice"
        context += f"[Source {source_number}] {row['title']} ({status})\n{row['chunk_text']}\n\n"

    return context.strip(), selected

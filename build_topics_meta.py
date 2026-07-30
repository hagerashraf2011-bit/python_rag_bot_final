"""
Regenerates data/topics_meta.json from 01_documents.py.
Run this whenever you add or rename a topic in 01_documents.py.
"""
import json
from collections import defaultdict
from importlib import import_module
from pathlib import Path

documents = import_module("01_documents").documents

# Display order + friendly bilingual labels for each internal category key.
CATEGORY_LABELS = {
    "basics": "🔤 Basics",
    "data_structures": "📦 Data Structures",
    "functions_functional": "🧩 Functions",
    "oop": "🏛️ OOP",
    "errors_files": "🛡️ Errors & Files",
    "modules_packages": "📚 Modules & Packages",
    "concurrency": "⚡ Concurrency",
    "professional_tools": "🛠️ Pro Tools",
    "advanced": "🚀 Advanced",
}
CATEGORY_ORDER = list(CATEGORY_LABELS.keys())


def build_topics_meta():
    categories = defaultdict(list)
    for doc in documents:
        categories[doc["category"]].append(doc["title"])

    ordered_keys = sorted(
        categories.keys(),
        key=lambda key: CATEGORY_ORDER.index(key) if key in CATEGORY_ORDER else 999,
    )

    return [
        {
            "category_key": category,
            "category": CATEGORY_LABELS.get(category, category),
            "topics": sorted(categories[category]),
        }
        for category in ordered_keys
    ]


if __name__ == "__main__":
    output_path = Path(__file__).resolve().parent / "data" / "topics_meta.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(build_topics_meta(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {sum(len(c['topics']) for c in build_topics_meta())} topics to {output_path}")

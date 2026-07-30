"""
Builds the Python knowledge base by scraping real pages from docs.python.org
(and packaging.python.org for the pip topic) instead of using hand-written text.

Run this once (and again whenever you edit data/sources.json):

    python 00_scrape_documents.py

Output: data/scraped_documents.json — a list of documents in the exact same
shape 01_documents.py already produces:
    {"id": ..., "title": ..., "category": ..., "is_current": True, "text": ...}
plus a "source_url" field for traceability.

01_documents.py automatically loads this file if it exists. If a topic can't
be scraped (offline, page moved, anchor renamed) that single topic silently
falls back to the original curated text instead of breaking the pipeline —
see _build_fallback_documents() in 01_documents.py. Nothing downstream
(02_preprocessing.py .. 07_prompting.py, streamlit_app.py) needs to change,
since they only ever see the same {id, title, category, is_current, text}
shape either way.

Raw HTML for each unique URL is cached under data/scrape_cache/ so re-runs
(e.g. after tweaking word limits) don't hammer docs.python.org.
"""
import hashlib
import json
import re
import sys
import time
from importlib import import_module
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
SOURCES_PATH = HERE / "data" / "sources.json"
OUTPUT_PATH = HERE / "data" / "scraped_documents.json"
CACHE_DIR = HERE / "data" / "scrape_cache"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; think-in-python-tutor-bot/1.0; "
                  "+https://docs.python.org educational RAG project)"
}
REQUEST_TIMEOUT = 15
REQUEST_DELAY = 0.3          # be polite between *new* requests
EXPLANATION_WORD_LIMIT = 200  # keeps the whole topic under one 250-word chunk (see README)
CODE_LINE_LIMIT = 12
HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")


def _cache_path(url: str) -> Path:
    return CACHE_DIR / f"{hashlib.md5(url.encode()).hexdigest()}.html"


def fetch_html(url: str, session: requests.Session) -> str:
    """Fetch a page, using an on-disk cache keyed by URL so repeated runs
    (and multiple topics that share the same page) don't re-download it."""
    cache_file = _cache_path(url)
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    response = session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    html = response.text

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(html, encoding="utf-8")
    time.sleep(REQUEST_DELAY)
    return html


def _clean_text(text: str) -> str:
    text = text.replace("\u00b6", "")  # Sphinx "¶" permalink marker
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _trim_words(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit])


def _section_scope(soup: BeautifulSoup, section_id: str):
    """Return the BeautifulSoup element that holds the content for a topic.

    docs.python.org (Sphinx) marks up pages a few different ways:
      - Prose sections are wrapped in <section id="...">...</section>
      - Function/method entries are <dt id="..."> followed by a <dd> with
        the description (e.g. functions.html#print, #enumerate)
      - Occasionally the id sits directly on a heading tag
    """
    if section_id is None:
        return soup.find("article") or soup.find("body") or soup

    target = soup.find(id=section_id)
    if target is None:
        return None

    if target.name == "section":
        return target
    if target.name == "dt":
        dd = target.find_next_sibling("dd")
        return dd if dd is not None else target
    if target.name in HEADING_TAGS:
        parent_section = target.find_parent("section")
        if parent_section is not None:
            return parent_section
        return target.parent
    return target


def extract_topic(html: str, section_id: str) -> tuple[str, str]:
    """Returns (explanation, code_example) extracted from one page section."""
    soup = BeautifulSoup(html, "lxml")
    scope = _section_scope(soup, section_id)
    if scope is None:
        raise ValueError(f"anchor #{section_id} not found on page")

    paragraphs = [
        _clean_text(p.get_text(" "))
        for p in scope.find_all("p", recursive=True)
    ]
    paragraphs = [p for p in paragraphs if p]
    explanation = " ".join(paragraphs)
    if not explanation:
        raise ValueError(f"no paragraph text found under #{section_id}")

    code_example = ""
    pre = scope.find("pre")
    if pre is not None:
        code_lines = pre.get_text("\n").splitlines()
        while code_lines and not code_lines[0].strip():
            code_lines.pop(0)
        while code_lines and not code_lines[-1].strip():
            code_lines.pop()
        code_example = "\n".join(code_lines[:CODE_LINE_LIMIT]).rstrip()

    return _trim_words(explanation, EXPLANATION_WORD_LIMIT), code_example


def build_document(source: dict, session: requests.Session, fallback_by_id: dict) -> dict:
    doc_id = source["id"]
    try:
        html = fetch_html(source["source_url"], session)
        explanation, code = extract_topic(html, source.get("section_id"))
        text = explanation
        if code:
            text += f"\nExample:\n{code}"
        elif doc_id in fallback_by_id:
            # Page had no runnable snippet; keep the curated example so the
            # bot still shows working code for this topic.
            fallback_code = fallback_by_id[doc_id]["text"].split("Example:", 1)
            if len(fallback_code) == 2:
                text += f"\nExample:{fallback_code[1]}"
        print(f"  [scraped] {doc_id}")
        return {
            "id": doc_id,
            "title": source["title"],
            "category": source["category"],
            "is_current": True,
            "text": text.strip(),
            "source_url": source["source_url"],
        }
    except Exception as exc:  # noqa: BLE001 - any scrape failure -> fallback
        print(f"  [fallback] {doc_id} ({exc})")
        fallback = fallback_by_id.get(doc_id)
        if fallback is None:
            raise
        return {**fallback, "source_url": source.get("source_url")}


def main():
    # Always start clean: delete any previous scraped output and cached
    # pages first, so re-running this script never silently keeps stale
    # data around — every run is a genuinely fresh scrape from
    # docs.python.org, not a reuse of whatever was cached last time.
    if OUTPUT_PATH.exists():
        OUTPUT_PATH.unlink()
        print(f"Removed previous {OUTPUT_PATH.relative_to(HERE)}")
    if CACHE_DIR.exists():
        cached_files = list(CACHE_DIR.glob("*.html"))
        for cached_file in cached_files:
            cached_file.unlink()
        print(f"Cleared {len(cached_files)} cached page(s) from {CACHE_DIR.relative_to(HERE)}")

    sources = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))

    # Curated text from 01_documents.py's built-in fallback, used per-topic
    # whenever scraping that specific topic fails (network, moved page, ...).
    fallback_docs = import_module("01_documents")._build_fallback_documents()
    fallback_by_id = {d["id"]: d for d in fallback_docs}

    session = requests.Session()
    documents = []

    print(f"Scraping {len(sources)} topics from docs.python.org (fresh run) ...")
    for source in sources:
        documents.append(build_document(source, session, fallback_by_id))

    OUTPUT_PATH.write_text(
        json.dumps(documents, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nWrote {len(documents)} documents to {OUTPUT_PATH.relative_to(HERE)}")
    print(f"Cached pages: {len(list(CACHE_DIR.glob('*.html'))) if CACHE_DIR.exists() else 0}")
    print("Run this again any time you edit data/sources.json — it will always re-scrape fresh.")


if __name__ == "__main__":
    sys.exit(main())

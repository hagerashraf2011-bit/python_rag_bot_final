"""
Runs a handful of test questions through all three prompt variants defined
in 07_prompting.py (minimal / grounded / grounded_currency) and saves a
side-by-side comparison — this is the "Three Prompts" comparison from the
original notebook, adapted to call the real pipeline (retrieval + LLM)
instead of being written by hand.

Run:
    python evaluation/compare_prompts.py

Requires a working LLM_API_KEY in .env (uses whichever provider/model is
configured — see 07_prompting.py).
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from importlib import import_module  # noqa: E402

prompting = import_module("07_prompting")
build_context = import_module("06_retrieve_context").build_context

# Deliberately includes one question that only an OUTDATED source answers
# (urllib2), so the comparison shows the real behavioral difference between
# grounded_currency and the two weaker variants.
TEST_QUESTIONS = [
    "How do I print something in Python?",
    "How do I install a package with distutils?",
    "How do I open a URL with urllib2?",
    "What is a list comprehension?",
]

VARIANTS = ["minimal", "grounded", "grounded_currency"]


def run_comparison():
    if not prompting.LLM_API_KEY:
        print("No LLM_API_KEY configured — set it in .env before running this script.")
        return

    report_lines = ["# Prompt Variant Comparison", ""]

    for question in TEST_QUESTIONS:
        context, sources = build_context(question)
        report_lines.append(f"## \"{question}\"")
        report_lines.append("")
        if not sources:
            report_lines.append("_No sources retrieved — skipped._\n")
            continue

        report_lines.append(f"Sources retrieved: {', '.join(s['title'] for s in sources)}")
        report_lines.append("")

        for variant_name in VARIANTS:
            builder = prompting.PROMPT_VARIANTS[variant_name]
            prompt = builder(question, context)
            print(f"Asking [{variant_name}] :: {question}")
            answer = prompting.ask_llm(prompt)
            report_lines.append(f"**{variant_name}:**")
            report_lines.append(f"> {answer}".replace("\n", "\n> "))
            report_lines.append("")

        report_lines.append("---\n")

    output_path = Path(__file__).resolve().parent / "prompt_comparison.md"
    output_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nWrote {output_path}")


if __name__ == "__main__":
    run_comparison()

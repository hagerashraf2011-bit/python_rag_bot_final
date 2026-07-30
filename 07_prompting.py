from importlib import import_module
import os

from dotenv import load_dotenv
from openai import OpenAI

build_context = import_module("06_retrieve_context").build_context

load_dotenv()

# Both Gemini and OpenRouter expose an OpenAI-compatible /chat/completions
# endpoint, so a single OpenAI() client works for either provider — only the
# base_url, api key, and model name change. This keeps requirements.txt small
# and makes it easy to switch providers by editing three env vars.
PROVIDER_BASE_URLS = {
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "openrouter": "https://openrouter.ai/api/v1",
}
DEFAULT_MODELS = {
    "gemini": "gemini-2.0-flash",
    "openrouter": "nvidia/nemotron-3-ultra-550b-a55b:free",
}

def _sanitize(value):
    """Strip whitespace and drop any non-ASCII character. API keys pasted
    from a web page sometimes carry an invisible character (smart quote,
    non-breaking space, zero-width space, BOM) that looks identical to a
    normal character but breaks HTTP header encoding with a
    UnicodeEncodeError. Stripping to plain ASCII removes it regardless of
    where it came from."""
    if not value:
        return ""
    return "".join(ch for ch in value.strip() if ord(ch) < 128)


LLM_PROVIDER = _sanitize(os.getenv("LLM_PROVIDER", "gemini")).lower() or "gemini"
LLM_API_KEY = _sanitize(os.getenv("LLM_API_KEY", ""))
LLM_MODEL = _sanitize(os.getenv("LLM_MODEL", "")) or DEFAULT_MODELS.get(LLM_PROVIDER, DEFAULT_MODELS["gemini"])

NO_MATCH_MESSAGE = (
    "I couldn't find this topic in my current Python knowledge base, so I'd "
    "rather not guess. Try rephrasing the question, or ask about one of the "
    "topics listed in the sidebar."
)


# ------------------------------------------------------------ prompt variants --
# Three prompt strategies, from weakest to strongest, kept side by side so
# they can be compared directly (see evaluation/compare_prompts.py and
# evaluation/error_analysis.md). The live app uses PROMPT_VARIANT (default:
# the strongest one) — override it in .env to try a different variant.

def build_prompt_minimal(question, context):
    """Weakest variant: no grounding discipline, no outdated-source handling.
    Kept as a baseline to show *why* the stronger variants below matter."""
    return f"""Answer the Python question using the context.

Question: {question}

Context:
{context}
"""


def build_prompt_grounded(question, context):
    """Middle variant: grounded and refuses to guess, but never tells the
    model what to do when a source is marked OUTDATED."""
    return f"""You are a friendly, knowledgeable Python tutor.

Answer using only the information in the context below — never mention the
context, sources, retrieval, or how you found the answer; just explain the
concept naturally, as a tutor would.

For every answer:
1. Give a short, clear explanation of the concept in plain language.
2. Include one small, correct Python code example inside a ```python code block.
3. Keep the tone encouraging and beginner-friendly.
4. Answer in the same language the student used to ask the question.
5. If the context truly does not cover the question, say so honestly and
   suggest the student rephrase — do not invent an answer.

Question:
{question}

Context:
{context}
"""


def build_prompt_grounded_currency(question, context):
    """Strongest variant: everything build_prompt_grounded does, plus
    explicit handling for sources marked (OUTDATED) in the context, which
    the conflict-resolution logic in 06_retrieve_context.py produces
    whenever a deprecated topic is retrieved."""
    return f"""You are a friendly, knowledgeable Python tutor.

Answer using only the information in the context below — never mention the
context, sources, retrieval, or how you found the answer; just explain the
concept naturally, as a tutor would.

For every answer:
1. Explain the concept thoroughly and clearly, in a few well-structured
   paragraphs: what it is, why/when you'd use it, and one common mistake or
   tip worth knowing. Do not pad with filler — every sentence should teach
   something real. You may elaborate with standard, well-known Python facts
   about this exact concept even if a specific phrasing isn't in the
   context verbatim, but never introduce unrelated topics or contradict
   the context.
2. Include a Python code example inside a ```python code block; if it helps
   the explanation, add a short second example or annotate the expected
   output as a comment.
3. Keep the tone encouraging and beginner-friendly.
4. Answer in the same language the student used to ask the question.
5. If the context truly does not cover the question, say so honestly and
   suggest the student rephrase — do not invent an answer.
6. Some context sources are labeled (OUTDATED). If the only source you have
   is marked OUTDATED, still answer, but clearly warn the student it's
   outdated and briefly mention the modern replacement if it's evident from
   the source text — do not present outdated syntax as current best practice.

Question:
{question}

Context:
{context}
"""


PROMPT_VARIANTS = {
    "minimal": build_prompt_minimal,
    "grounded": build_prompt_grounded,
    "grounded_currency": build_prompt_grounded_currency,
}
PROMPT_VARIANT = os.getenv("PROMPT_VARIANT", "grounded_currency").strip().lower()
build_prompt = PROMPT_VARIANTS.get(PROMPT_VARIANT, build_prompt_grounded_currency)


def ask_llm(prompt):
    client = OpenAI(
        base_url=PROVIDER_BASE_URLS.get(LLM_PROVIDER, PROVIDER_BASE_URLS["gemini"]),
        api_key=LLM_API_KEY,
    )

    # Free-tier models occasionally return a response with no choices (empty
    # completion, momentary provider hiccup) instead of raising an error.
    # Retry once before giving the student a clear, non-crashing message.
    for attempt in range(2):
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content

    return (
        "The model didn't return an answer just now (this can happen with "
        "free-tier models under load). Please try asking again."
    )


def answer_question(question):
    context, sources = build_context(question)

    if not sources:
        return NO_MATCH_MESSAGE, sources

    if not LLM_API_KEY:
        return "Missing LLM_API_KEY. Add it to your .env file or Streamlit secrets.", sources

    prompt = build_prompt(question, context)
    return ask_llm(prompt), sources

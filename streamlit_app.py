import json
import time
from importlib import import_module
from pathlib import Path

import streamlit as st

rag = import_module("07_prompting")

# Read the API key/model from Streamlit secrets when deployed and no local
# .env is present, so the same code works locally and on Streamlit Cloud.
try:
    if not rag.LLM_API_KEY:
        rag.LLM_API_KEY = rag._sanitize(st.secrets.get("LLM_API_KEY", ""))
    rag.LLM_PROVIDER = rag._sanitize(st.secrets.get("LLM_PROVIDER", rag.LLM_PROVIDER)) or rag.LLM_PROVIDER
    rag.LLM_MODEL = rag._sanitize(st.secrets.get("LLM_MODEL", rag.LLM_MODEL)) or rag.LLM_MODEL
except Exception:
    pass

st.set_page_config(page_title="Think in Python.", page_icon="🐍", layout="centered")

# Any button (sidebar topic, related topic, mode switch) stages its change
# here instead of writing directly to a widget's session-state key, because
# Streamlit forbids writing to a widget's key after that widget has already
# been instantiated in the same script run. Syncing it here, before any
# widget below is created, avoids that restriction entirely.
if "pending_question" in st.session_state:
    st.session_state["question"] = st.session_state.pop("pending_question")
if "question" not in st.session_state:
    st.session_state["question"] = ""
if "mode" not in st.session_state:
    st.session_state["mode"] = "ask"


def _ask_about(topic_title):
    st.session_state["pending_question"] = f"What is {topic_title}?"
    st.session_state["auto_run"] = True
    st.session_state["mode"] = "ask"


def _switch_mode(mode):
    st.session_state["mode"] = mode


DATA_DIR = Path(__file__).resolve().parent / "data"

try:
    topics_by_category = json.loads((DATA_DIR / "topics_meta.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    topics_by_category = []

try:
    problems = json.loads((DATA_DIR / "problems.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    problems = []

PROBLEM_TOPICS = sorted({p["topic"] for p in problems})
TIMER_SECONDS = {"Easy": 60, "Medium": 120, "Hard": 180}

# ---------------------------------------------------------------- styling ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Nunito:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

    /* Streamlit renders its own icons (like the expander arrow) using a
       Material icon font on a span with this testid. Our broad Nunito
       font-family rules above/below accidentally override it, which makes
       the icon show up as literal text (e.g. "arrow_right") instead of a
       glyph. Force the icon font back with higher priority. */
    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Icons' !important;
    }

    /* bright, cheerful backdrop instead of a dark developer-tool panel */
    .stApp {
        background-color: #EAE6F7;
        background-image: radial-gradient(circle at 1px 1px, rgba(124,77,255,0.10) 1.5px, transparent 0);
        background-size: 26px 26px;
        color: #3c3c3c;
    }

    section[data-testid="stSidebar"] {
        background-color: #F4F1FB;
        border-right: 3px solid #ddd4f2;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] summary,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stCaption {
        color: #3c3c3c !important;
        font-family: 'Nunito', sans-serif;
    }
    section[data-testid="stSidebar"] .stButton button {
        background: #ffffff !important;
        color: #4b4b4b !important;
        border: 2px solid #e5e5e5 !important;
        border-bottom: 4px solid #d8d8d8 !important;
        text-align: left !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-family: 'Nunito', sans-serif !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        border-color: #7C4DFF !important;
        color: #7C4DFF !important;
    }
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
        background-color: #f7f7f7;
        border-radius: 14px;
        font-weight: 800;
        color: #3c3c3c;
    }

    /* hero header — playful rounded card, big bouncy title */
    .repl-header {
        font-family: 'Baloo 2', cursive;
        background: linear-gradient(135deg, #7C4DFF 0%, #6A3DE8 100%);
        border-radius: 24px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow: 0 6px 0 #5A32C7;
    }
    .repl-header .prompt { display: none; }
    .repl-header .title {
        font-family: 'Baloo 2', cursive;
        font-weight: 800;
        font-size: 2.1rem;
        color: #ffffff;
        margin: 0 0 4px 0;
    }
    .repl-header .subtitle { color: #eaffda; font-size: 1rem; font-weight: 600; font-family: 'Nunito', sans-serif; }

    /* pill-tab mode switcher — big friendly toggle chips */
    div[data-testid="column"] .stButton button {
        border-radius: 999px !important;
        font-family: 'Baloo 2', cursive !important;
        font-size: 1.05rem !important;
    }
    .mode-tab-active button {
        background: #7C4DFF !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: none !important;
        border-bottom: 4px solid #5A32C7 !important;
    }
    .mode-tab-inactive button {
        background: #ffffff !important;
        color: #afafaf !important;
        border: 2px solid #e5e5e5 !important;
        border-bottom: 4px solid #d8d8d8 !important;
    }

    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #3c3c3c !important;
        border: 2px solid #e5e5e5 !important;
        border-radius: 16px !important;
        font-family: 'Nunito', sans-serif;
    }
    .stTextArea textarea:focus {
        border-color: #1cb0f6 !important;
    }

    /* chunky "3D" buttons — press-down shadow like a game UI */
    .stButton button {
        background: #7C4DFF;
        color: #ffffff;
        border: none;
        font-weight: 800;
        font-family: 'Baloo 2', cursive;
        border-radius: 14px;
        border-bottom: 4px solid #5A32C7;
        transition: transform 0.08s ease;
    }
    .stButton button:hover {
        background: #9670FF;
    }
    .stButton button:active {
        transform: translateY(3px);
        border-bottom: 1px solid #5A32C7;
    }

    .answer-box {
        background: #ffffff;
        border: 2px solid #ddf4c2;
        border-left: 6px solid #7C4DFF;
        border-radius: 18px;
        padding: 20px 22px;
        margin-top: 14px;
        color: #3c3c3c;
    }
    .answer-box code, .answer-box pre { border-radius: 10px; }

    /* practice-mode problem card — playful, rounded, colorful badges */
    .problem-card {
        background: #ffffff;
        border: 2px solid #e5e5e5;
        border-radius: 20px;
        padding: 22px 24px;
        margin-top: 10px;
        box-shadow: 0 4px 0 #e5e5e5;
    }
    .problem-card .badge {
        display: inline-block;
        font-family: 'Baloo 2', cursive;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 4px 14px;
        border-radius: 999px;
        margin-right: 6px;
    }
    .badge-easy { background: #d7f8c2; color: #5A32C7; }
    .badge-medium { background: #fff3c4; color: #b8860b; }
    .badge-hard { background: #ffd6d6; color: #c0392b; }
    .badge-topic { background: #d3ecfb; color: #1899d6; }
    .problem-card h3 { margin: 10px 0 6px 0; color: #3c3c3c; font-family: 'Baloo 2', cursive; }
    .problem-card p { color: #4b4b4b; font-family: 'Nunito', sans-serif; }

    .timer-display {
        font-family: 'Baloo 2', cursive;
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        padding: 10px 0;
        color: #1cb0f6;
    }
    .timer-display.low { color: #ff4b4b; }
    .times-up-banner {
        font-family: 'Baloo 2', cursive;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 800;
        color: #7C4DFF;
        padding: 8px 0 4px 0;
    }

    /* topic pill buttons in Practice mode: smaller readable font, clean
       word-wrapping (no mid-word breaks), consistent height across rows */
    .topic-pill .stButton button {
        font-size: 0.85rem !important;
        white-space: normal !important;
        line-height: 1.25 !important;
        min-height: 52px;
        padding: 6px 10px !important;
        word-break: keep-all;
    }

    /* VS-Code-dark style for every code block, in both Ask answers and
       Practice mode solutions — deliberately different from the light page
       background so code always reads like a real editor. */
    .stCodeBlock, div[data-testid="stCodeBlock"] {
        background-color: #1e1e1e !important;
        border-radius: 10px !important;
        border: 1px solid #3c3c3c !important;
    }
    .stCodeBlock pre, div[data-testid="stCodeBlock"] pre,
    .stCodeBlock code, div[data-testid="stCodeBlock"] code {
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .answer-box pre, .answer-box code {
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .answer-box code:not(pre code) {
        padding: 2px 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ header ---
st.markdown(
    """
    <div class="repl-header">
        <span class="prompt">&gt;&gt;&gt;</span> <span class="title">🐍 Think in Python!</span>
        <div class="subtitle">Ask any Python question, or practice with timed coding problems.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------- mode switch ---
tab_col1, tab_col2, _spacer = st.columns([1, 1, 3])
with tab_col1:
    st.markdown(f'<div class="mode-tab-{"active" if st.session_state["mode"] == "ask" else "inactive"}">', unsafe_allow_html=True)
    st.button("💬 Ask", key="mode_ask", on_click=_switch_mode, args=("ask",), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with tab_col2:
    st.markdown(f'<div class="mode-tab-{"active" if st.session_state["mode"] == "practice" else "inactive"}">', unsafe_allow_html=True)
    st.button("🧩 Practice", key="mode_practice", on_click=_switch_mode, args=("practice",), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ sidebar --
with st.sidebar:
    st.markdown("### 🐍 Browse topics")
    st.caption("Tap a topic to ask about it directly.")
    for group in topics_by_category:
        with st.expander(f"{group['category']} ({len(group['topics'])})"):
            for topic in group["topics"]:
                st.button(
                    topic,
                    key=f"topic_{topic}",
                    use_container_width=True,
                    on_click=_ask_about,
                    args=(topic,),
                )

    st.markdown("### 🔑 API Key")
    with st.expander("Use your own key for this session"):
        st.caption(
            "Optional. If you have your own free Gemini or OpenRouter key, "
            "paste it here to use it just for your session — nothing is saved."
        )
        user_provider = st.selectbox("Provider", ["gemini", "openrouter"], key="user_provider")
        user_key = st.text_input("API Key", type="password", key="user_api_key")
        user_model = st.text_input(
            "Model (optional)",
            key="user_model",
            placeholder="leave blank for the default model",
        )
        if st.button("Use this key", key="apply_user_key", use_container_width=True):
            cleaned_key = rag._sanitize(user_key)
            if cleaned_key:
                rag.LLM_PROVIDER = user_provider
                rag.LLM_API_KEY = cleaned_key
                rag.LLM_MODEL = rag._sanitize(user_model) or rag.DEFAULT_MODELS.get(user_provider, rag.DEFAULT_MODELS["gemini"])
                st.success("Using your key for this session.")
            else:
                st.error("Please paste a key first.")

    if not rag.LLM_API_KEY:
        st.warning("No LLM_API_KEY configured yet — add it to .env, Streamlit secrets, or paste your own key above.")

# ============================================================== ASK MODE ===
if st.session_state["mode"] == "ask":
    question = st.text_area(
        ">>> ask me anything about Python",
        key="question",
        height=90,
        placeholder="e.g. What is a list comprehension?",
    )
    st.caption("💡 Works best with questions written in English.")

    run_clicked = st.button("Run")
    auto_run = st.session_state.pop("auto_run", False)

    if (run_clicked or auto_run) and question.strip():
        with st.spinner("Thinking..."):
            answer, sources = rag.answer_question(question)

        st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

        if sources:
            st.markdown("**Related topics — click to ask about one:**")
            cols = st.columns(len(sources))
            for col, s in zip(cols, sources):
                with col:
                    st.button(
                        s["title"],
                        key=f"related_{s['title']}",
                        use_container_width=True,
                        on_click=_ask_about,
                        args=(s["title"],),
                    )

# =========================================================== PRACTICE MODE ===
else:
    if not problems:
        st.warning("No problems found in data/problems.json.")
    else:
        st.markdown("#### Pick a topic to practice")
        TOPICS_PER_ROW = 4
        for row_start in range(0, len(PROBLEM_TOPICS), TOPICS_PER_ROW):
            row_topics = PROBLEM_TOPICS[row_start:row_start + TOPICS_PER_ROW]
            topic_cols = st.columns(TOPICS_PER_ROW)
            for col, topic in zip(topic_cols, row_topics):
                count = sum(1 for p in problems if p["topic"] == topic)
                with col:
                    st.markdown('<div class="topic-pill">', unsafe_allow_html=True)
                    if st.button(f"{topic} ({count})", key=f"practice_topic_{topic}", use_container_width=True):
                        st.session_state["practice_topic"] = topic
                        st.session_state["practice_index"] = 0
                        st.session_state["show_answer"] = False
                    st.markdown("</div>", unsafe_allow_html=True)

        current_topic = st.session_state.get("practice_topic")

        if current_topic:
            topic_problems = [p for p in problems if p["topic"] == current_topic]
            idx = st.session_state.get("practice_index", 0) % len(topic_problems)
            problem = topic_problems[idx]
            difficulty_class = {"Easy": "badge-easy", "Medium": "badge-medium", "Hard": "badge-hard"}.get(problem["difficulty"], "badge-medium")
            duration = TIMER_SECONDS.get(problem["difficulty"], 60)

            st.markdown(
                f"""
                <div class="problem-card">
                    <span class="badge badge-topic">{problem['topic']}</span>
                    <span class="badge {difficulty_class}">{problem['difficulty']}</span>
                    <h3>{problem['title']}</h3>
                    <p>{problem['question']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            with btn_col1:
                start_clicked = st.button(f"▶ Start Timer ({duration}s)", key=f"start_{problem['id']}", use_container_width=True)
            with btn_col2:
                hint_clicked = st.button("💡 Give me a hint", key=f"hint_{problem['id']}", use_container_width=True)
            with btn_col3:
                show_now_clicked = st.button("👁 Show Answer Now", key=f"show_{problem['id']}", use_container_width=True)
            with btn_col4:
                next_clicked = st.button("⏭ Next Problem", key=f"next_{problem['id']}", use_container_width=True)

            if next_clicked:
                st.session_state["practice_index"] = idx + 1
                st.session_state["show_answer"] = False
                st.rerun()

            if hint_clicked:
                hint_text = problem.get("hint", "No hint available for this problem — give it your best shot!")
                st.info(f"💡 **Hint:** {hint_text}")

            reveal = show_now_clicked or st.session_state.get("show_answer", False)

            if start_clicked and not reveal:
                timer_placeholder = st.empty()
                for remaining in range(duration, 0, -1):
                    css_class = "timer-display low" if remaining <= 10 else "timer-display"
                    timer_placeholder.markdown(
                        f'<div class="{css_class}">⏱ {remaining}s</div>', unsafe_allow_html=True
                    )
                    time.sleep(1)
                timer_placeholder.markdown(
                    '<div class="times-up-banner">⏰ Time\'s up! Here\'s the solution:</div>',
                    unsafe_allow_html=True,
                )
                st.balloons()
                reveal = True

            if reveal:
                st.markdown("**✅ Solution:**")
                st.code(problem["solution_code"], language="python")
                st.markdown(f"**Explanation:** {problem['explanation']}")
                if problem.get("expected_output"):
                    st.markdown("**Expected Output:**")
                    st.code(problem["expected_output"], language="text")

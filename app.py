"""Japan Carry Trade Q&A — Creative & Visual Edition."""

import random

import streamlit as st
from openai import OpenAI
from pathlib import Path
from streamlit_lottie import st_lottie

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

APP_TITLE = "Japan Carry Trade Q&A"
CASE_DATA_PATH = Path(__file__).parent / "case_data" / "japan_carry_trade.md"

SYSTEM_PROMPT_TEMPLATE = """\
You are an expert on the Japan Carry Trade case study from MGMT 69000: \
Mastering AI for Finance at Purdue University. Your role is to help students \
understand the 2024 yen carry trade unwind, the contagion mechanism, \
transfer entropy analysis, and the DRIVER framework application.

Answer questions using ONLY the case material provided below. If a question \
falls outside the scope of this case, say so clearly. Be precise with data \
points (dates, percentages, levels). When explaining transfer entropy, \
emphasize the directional/asymmetric nature vs. symmetric correlation.

Use emojis in your responses to make them more engaging and easier to scan. \
For example, use 📊 for data points, ⚠️ for warnings/risks, 💡 for key \
insights, 🔗 for connections between concepts, and 📅 for dates.

--- CASE MATERIAL ---
{case_content}
--- END CASE MATERIAL ---
"""

EXAMPLE_QUESTIONS = [
    ("💥", "What happened on August 5, 2024?"),
    ("📊", "How does transfer entropy differ from correlation?"),
    ("🔗", "What is the contagion chain in the carry trade unwind?"),
    ("📉", "Why did correlation fail during the stress event?"),
    ("🧭", "How does the DRIVER framework apply to this case?"),
    ("🔮", "What is the Markov perspective on the BOJ policy shift?"),
]

DID_YOU_KNOW_FACTS = [
    "🏦 The yen carry trade was estimated at **$4 trillion** globally before the unwind.",
    "📉 On Aug 5, 2024, Topix dropped **12%** — its worst day since 1987's Black Monday.",
    "💱 USD/JPY swung from **161 to 142** in just weeks — a massive 12% move for a major pair.",
    "📊 Transfer entropy can detect information flow that correlation completely misses.",
    "🌊 The VIX spiked above **60** during the unwind — levels seen only in extreme crises.",
    "🇯🇵 The BOJ kept rates at or below zero for over **two decades** before the 2024 shift.",
    "🔗 Contagion spread from Tokyo → to US tech → to crypto in under 48 hours.",
]

TIMELINE_EVENTS = [
    ("🏦", "Mar 19, 2024", "BOJ ends negative interest rate policy — first hike since 2007"),
    ("💱", "Jul 2024", "USD/JPY hits 161 — yen at weakest level in decades"),
    ("⚡", "Jul 31, 2024", "BOJ surprises with second rate hike to 0.25%"),
    ("🌪️", "Aug 1–2, 2024", "Rapid yen appreciation begins; carry trades start unwinding"),
    ("💥", "Aug 5, 2024", "**Black Monday** — Topix crashes 12%, Nikkei -12.4%"),
    ("📈", "Aug 5, 2024", "VIX spikes above 60; global contagion spreads"),
    ("🔄", "Aug 6–7, 2024", "BOJ signals pause; partial market recovery begins"),
    ("📊", "Post-crisis", "Transfer entropy analysis reveals hidden directional flows"),
]

LOTTIE_FINANCE_URL = "https://lottie.host/4db68bbd-31f6-4cd8-84eb-189571e57b25/AQMHYDhDSK.json"

# ---------------------------------------------------------------------------
# CSS Animations
# ---------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@keyframes pulse-glow {
    0%, 100% { text-shadow: 0 0 10px rgba(255, 69, 0, 0.3); }
    50% { text-shadow: 0 0 25px rgba(255, 69, 0, 0.7), 0 0 40px rgba(255, 165, 0, 0.4); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

@keyframes fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    animation: pulse-glow 3s ease-in-out infinite;
    text-align: center;
    padding: 0.5rem 0 0 0;
    margin-bottom: 0;
}

.bouncing-yen {
    text-align: center;
    font-size: 1.8rem;
    animation: bounce 2s ease-in-out infinite;
    margin: 0;
    padding: 0;
}

.hero-caption {
    text-align: center;
    color: #888;
    font-size: 0.95rem;
    margin-top: 0.2rem;
}

/* Fade-in for chat messages */
.stChatMessage {
    animation: fade-in 0.5s ease-out;
}

/* Metric card styling */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Timeline styling */
.timeline-item {
    padding: 8px 0;
    border-left: 3px solid #e94560;
    padding-left: 16px;
    margin-left: 8px;
    margin-bottom: 4px;
}
</style>
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@st.cache_data
def load_case_content() -> str:
    """Load the case study markdown file."""
    return CASE_DATA_PATH.read_text(encoding="utf-8")


def build_system_prompt(case_content: str) -> str:
    """Inject case content into the system prompt template."""
    return SYSTEM_PROMPT_TEMPLATE.format(case_content=case_content)


def load_lottie_url(url: str) -> dict | None:
    """Fetch a Lottie animation JSON from a URL."""
    import requests

    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def render_sidebar(case_content: str) -> dict:
    """Render sidebar with case overview, settings, and example questions."""
    with st.sidebar:
        # Lottie animation
        lottie_data = load_lottie_url(LOTTIE_FINANCE_URL)
        if lottie_data:
            st_lottie(lottie_data, height=150, key="sidebar_lottie")

        st.header("📚 About This Case")
        st.markdown(
            "**Case 5 — Japan Carry Trade Unwind (2024)**\n\n"
            "Explore the mechanics of the yen carry trade, the August 5 Black "
            "Monday crash, contagion mechanisms, and how transfer entropy "
            "reveals directional information flow in financial markets."
        )

        st.divider()

        # Did You Know? box
        if "fun_fact" not in st.session_state:
            st.session_state.fun_fact = random.choice(DID_YOU_KNOW_FACTS)
        st.info(f"🎲 **Did You Know?**\n\n{st.session_state.fun_fact}")

        st.divider()
        st.subheader("❓ Example Questions")
        for emoji, q in EXAMPLE_QUESTIONS:
            if st.button(f"{emoji} {q}", key=q, use_container_width=True):
                st.session_state["prefill_question"] = q

        st.divider()
        st.subheader("⚙️ Settings")
        model = st.selectbox(
            "Model",
            ["gpt-4.1", "gpt-4o-mini", "gpt-4.1-mini"],
            index=0,
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

        st.divider()

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("welcomed", None)
            st.session_state.pop("first_question_asked", None)
            st.rerun()

        st.divider()
        st.caption(
            "🎓 MGMT 69000 · Mastering AI for Finance · **Purdue University**"
        )

    return {"model": model, "temperature": temperature}


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="💹",
        layout="centered",
    )

    # Inject custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ── Animated Hero Header ──
    st.markdown(
        '<div class="hero-title">🇯🇵💹 Japan Carry Trade Q&A 🏯</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="bouncing-yen">¥</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-caption">AI-powered Q&A grounded in the Japan Carry Trade case study</div>',
        unsafe_allow_html=True,
    )

    # ── Key Stats Dashboard ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📉 Topix Drop", value="-12%", delta="Aug 5")
    with col2:
        st.metric(label="😱 VIX Spike", value=">60", delta="Extreme")
    with col3:
        st.metric(label="💱 USD/JPY", value="161→142", delta="-12%")
    with col4:
        st.metric(label="🏦 BOJ Rate", value="0.25%", delta="First hike")

    # ── Visual Timeline ──
    with st.expander("📅 Event Timeline — Key Dates of the Carry Trade Unwind"):
        for emoji, date, description in TIMELINE_EVENTS:
            st.markdown(
                f'<div class="timeline-item">'
                f"<strong>{emoji} {date}</strong><br>{description}</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    # Load case content and build system prompt
    case_content = load_case_content()
    system_prompt = build_system_prompt(case_content)
    settings = render_sidebar(case_content)

    # Initialize OpenAI client
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if not api_key:
        st.warning(
            "⚠️ Please set your OpenAI API key in `.streamlit/secrets.toml` "
            "or as an environment variable `OPENAI_API_KEY`."
        )
        st.stop()

    client = OpenAI(api_key=api_key)

    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome message on first load
    if not st.session_state.get("welcomed"):
        st.session_state.welcomed = True
        welcome = (
            "👋 Hey! I'm your **Japan Carry Trade expert**. Ask me anything "
            "about the 2024 yen carry trade unwind, the Black Monday crash, "
            "contagion mechanisms, or transfer entropy analysis.\n\n"
            "💡 *Try one of the example questions in the sidebar to get started!*"
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome}
        )

    # Display chat history with custom avatars
    for msg in st.session_state.messages:
        avatar = "🧑‍🎓" if msg["role"] == "user" else "🏦"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Handle prefilled question from sidebar button
    prefill = st.session_state.pop("prefill_question", None)
    prompt = st.chat_input("Ask about the Japan Carry Trade… 💬") or prefill

    if prompt:
        # Easter egg: balloons on first question
        if not st.session_state.get("first_question_asked"):
            st.session_state.first_question_asked = True
            st.balloons()

        # Easter egg: snow for crash/Black Monday mentions
        prompt_lower = prompt.lower()
        if "black monday" in prompt_lower or "crash" in prompt_lower:
            st.snow()

        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)

        # Build messages for API call
        api_messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # Stream assistant response
        with st.chat_message("assistant", avatar="🏦"):
            stream = client.chat.completions.create(
                model=settings["model"],
                messages=api_messages,
                temperature=settings["temperature"],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )


if __name__ == "__main__":
    main()

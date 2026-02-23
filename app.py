"""Japan Carry Trade Q&A — Creative & Visual Edition."""

import random

import streamlit as st
import openai
from openai import OpenAI
from pathlib import Path
from streamlit_lottie import st_lottie

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

APP_TITLE = "Japan Carry Trade Q&A"
CASE_DATA_PATH = Path(__file__).parent / "case_data" / "japan_carry_trade.md"

SYSTEM_PROMPT_TEMPLATE = """\
You are a funny, slightly sarcastic (but honest and accurate) expert on the \
Japan Carry Trade case study from MGMT 69000: Mastering AI for Finance at \
Purdue University. You help students understand the 2024 yen carry trade \
unwind, contagion mechanisms, transfer entropy, and the DRIVER framework.

YOUR PERSONALITY:
- You're like a witty finance friend who actually knows their stuff
- Sprinkle in reactions like "ugh", "cute", "yikes", "bestie", "not gonna \
lie", "slay", "lowkey", "the audacity", "no because seriously" naturally
- Be a little dramatic about the numbers — because they ARE dramatic
- Use sarcasm when talking about bad decisions (like ignoring tail risk for \
17 years lol), but always follow up with the real explanation
- Keep it educational — the sass is the vehicle, the knowledge is the cargo
- If something is genuinely wild (VIX >60, $4T unwind), react like a human \
would: "excuse me WHAT"
- If a question is outside the case, say so — but make it funny: "bestie \
that's a great question but it's not in my case notes, I'm not gonna \
make stuff up for you"

RULES:
- Answer using ONLY the case material below. Be precise with data points.
- When explaining transfer entropy, emphasize directional/asymmetric nature \
vs. symmetric correlation.
- Use emojis generously: 📊 data, ⚠️ warnings, 💡 insights, 🔗 connections, \
📅 dates, 💀 for things that went badly, ✨ for key moments

--- CASE MATERIAL ---
{case_content}
--- END CASE MATERIAL ---
"""

EXAMPLE_QUESTIONS = [
    ("💥", "What on earth happened on August 5, 2024?"),
    ("📊", "Transfer entropy vs correlation — what's the tea?"),
    ("🔗", "Walk me through the contagion chain (the drama)"),
    ("📉", "Why did correlation ghost us during the crash?"),
    ("🧭", "How does DRIVER apply here? (yes I did the reading)"),
    ("🔮", "Markov perspective on BOJ — was anyone paying attention?"),
]

DID_YOU_KNOW_FACTS = [
    "🏦 The yen carry trade was worth **$4 trillion**. Four. Trillion. And people acted surprised when it blew up. Cute.",
    "📉 Topix dropped **12%** on Aug 5 — worst day since 1987. Ugh, imagine checking your portfolio that morning.",
    "💱 USD/JPY went from **161 to 142** in weeks. A 12% move on a major currency pair is *unhinged*.",
    "📊 Transfer entropy catches information flow that correlation completely misses. Correlation could never.",
    "🌊 VIX spiked above **60**. That's COVID-level panic. On a Monday. In August. The audacity.",
    "🇯🇵 BOJ kept rates at zero for **17+ years** and everyone just… built their whole strategy around it? Yikes.",
    "🔗 Contagion went Tokyo → US tech → crypto in **under 48 hours**. Speed run, honestly.",
    "💀 Hedge funds sized positions for a world where BOJ *never* hikes. Narrator: they hiked.",
    "✨ Transfer entropy literally answers 'who started it' — it's the group chat receipts of finance.",
]

TIMELINE_EVENTS = [
    ("🏦", "Mar 19, 2024", "BOJ ends negative rates — first hike since 2007. *Everyone: it's fine, right?*"),
    ("💱", "Jul 2024", "USD/JPY hits 161. Yen is basically on sale. Everyone is still vibing."),
    ("⚡", "Jul 31, 2024", "BOJ drops a SECOND rate hike to 0.25%. Markets: *wait, you're serious??*"),
    ("🌪️", "Aug 1–2, 2024", "Yen starts ripping higher. Carry trades unwinding. Cue the panic."),
    ("💥", "Aug 5, 2024", "**Black Monday** — Topix -12%, Nikkei -12.4%. Portfolios in shambles."),
    ("😱", "Aug 5, 2024", "VIX spikes above 60. That's not a number, that's a cry for help."),
    ("🔄", "Aug 6–7, 2024", "BOJ: 'jk we'll chill.' Markets partially recover. Trust issues remain."),
    ("📊", "Post-crisis", "Transfer entropy shows who actually started the mess. Receipts secured."),
]

LOTTIE_FINANCE_URL = "https://lottie.host/4db68bbd-31f6-4cd8-84eb-189571e57b25/AQMHYDhDSK.json"
LOTTIE_CHART_URL = "https://lottie.host/e4bd4e6c-5bce-4193-978d-157cd7c12e50/AlVlCjKDJH.json"

CONTAGION_FLOW_STEPS = [
    {"label": "Tokyo 🇯🇵", "detail": "BOJ said 'surprise!' — yen goes brrr"},
    {"label": "US Tech 🇺🇸", "detail": "Margin calls enter the chat"},
    {"label": "Crypto ₿", "detail": "Liquidation cascade — oof"},
    {"label": "Global 🌍", "detail": "VIX >60. Everyone panics. Cute."},
]

# ---------------------------------------------------------------------------
# CSS Animations
# ---------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
/* ── Keyframes ── */
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

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float-up {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10% { opacity: 0.7; }
    90% { opacity: 0.7; }
    100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
}

@keyframes glow-sweep {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes scroll-left {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

@keyframes contagion-pulse {
    0%, 100% { opacity: 0.4; text-shadow: none; }
    50% { opacity: 1; text-shadow: 0 0 12px rgba(233, 69, 96, 0.8); }
}

@keyframes pulse-dot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.6; }
}

/* ── 1. Animated Gradient Background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(270deg, #0a0a1a, #1a0a2e, #0a1a2e, #0a0a1a);
    background-size: 600% 600%;
    animation: gradient-shift 20s ease infinite;
}

/* ── 2. Floating Financial Symbols ── */
.floating-symbols {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.floating-symbols span {
    position: absolute;
    bottom: -5vh;
    font-size: 1.5rem;
    opacity: 0;
    animation: float-up linear infinite;
}
.floating-symbols span:nth-child(1) { left: 5%; animation-duration: 14s; animation-delay: 0s; }
.floating-symbols span:nth-child(2) { left: 15%; animation-duration: 18s; animation-delay: 2s; }
.floating-symbols span:nth-child(3) { left: 25%; animation-duration: 12s; animation-delay: 4s; }
.floating-symbols span:nth-child(4) { left: 40%; animation-duration: 16s; animation-delay: 1s; }
.floating-symbols span:nth-child(5) { left: 55%; animation-duration: 20s; animation-delay: 3s; }
.floating-symbols span:nth-child(6) { left: 65%; animation-duration: 13s; animation-delay: 5s; }
.floating-symbols span:nth-child(7) { left: 75%; animation-duration: 17s; animation-delay: 2.5s; }
.floating-symbols span:nth-child(8) { left: 88%; animation-duration: 15s; animation-delay: 0.5s; }
.floating-symbols span:nth-child(9) { left: 35%; animation-duration: 19s; animation-delay: 6s; }
.floating-symbols span:nth-child(10) { left: 92%; animation-duration: 14s; animation-delay: 3.5s; }

/* ── Hero ── */
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    animation: pulse-glow 3s ease-in-out infinite;
    text-align: center;
    padding: 0.5rem 0 0 0;
    margin-bottom: 0;
    position: relative;
    z-index: 1;
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

/* ── Fade-in for chat messages ── */
.stChatMessage {
    animation: fade-in 0.5s ease-out;
}

/* ── 4. Metric Card Enhancements ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
    animation: fade-in 0.6s ease-out both;
}
div[data-testid="stMetric"]:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3);
}
div[data-testid="stMetric"]::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.06) 50%, transparent 100%);
    background-size: 200% 100%;
    animation: shimmer 3s ease-in-out infinite;
    pointer-events: none;
}
/* Staggered entrance for metric cards */
div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stMetric"] { animation-delay: 0s; }
div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stMetric"] { animation-delay: 0.2s; }
div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stMetric"] { animation-delay: 0.4s; }
div[data-testid="stHorizontalBlock"] > div:nth-child(4) div[data-testid="stMetric"] { animation-delay: 0.6s; }

/* ── 3. Glowing Neon Dividers ── */
.glow-divider {
    border: none;
    height: 2px;
    margin: 1.5rem 0;
    background: linear-gradient(90deg, transparent, #e94560, #0f3460, #e94560, transparent);
    background-size: 200% 100%;
    animation: glow-sweep 3s linear infinite;
    border-radius: 2px;
}

/* ── 6. Ticker Tape Banner ── */
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: rgba(15, 52, 96, 0.4);
    border: 1px solid rgba(233, 69, 96, 0.2);
    border-radius: 6px;
    padding: 8px 0;
    margin: 0.5rem 0 1rem 0;
}
.ticker-content {
    display: inline-block;
    white-space: nowrap;
    animation: scroll-left 25s linear infinite;
    font-family: monospace;
    font-size: 0.85rem;
    color: #e94560;
    letter-spacing: 0.5px;
}
.ticker-content span {
    padding: 0 2rem;
}

/* ── 5. Contagion Flow Diagram ── */
.contagion-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 1.5rem 0;
}
.contagion-step {
    text-align: center;
    padding: 12px 18px;
    background: rgba(26, 26, 46, 0.8);
    border: 1px solid #0f3460;
    border-radius: 10px;
    min-width: 120px;
    transition: transform 0.3s ease;
}
.contagion-step:hover {
    transform: scale(1.08);
}
.contagion-step .label {
    font-size: 1.1rem;
    font-weight: 700;
}
.contagion-step .detail {
    font-size: 0.75rem;
    color: #888;
    margin-top: 4px;
}
.contagion-arrow {
    font-size: 1.4rem;
    animation: contagion-pulse 2s ease-in-out infinite;
}
.contagion-arrow:nth-child(4) { animation-delay: 0.5s; }
.contagion-arrow:nth-child(6) { animation-delay: 1.0s; }
.contagion-arrow:nth-child(8) { animation-delay: 1.5s; }

/* ── 7. Sidebar Button Hover Effects ── */
section[data-testid="stSidebar"] button {
    transition: all 0.3s ease !important;
    border: 1px solid transparent !important;
}
section[data-testid="stSidebar"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
    border-color: #e94560 !important;
    color: #e94560 !important;
}

/* ── 8. Staggered Timeline Animation ── */
.timeline-item {
    padding: 8px 0;
    border-left: 3px solid #e94560;
    padding-left: 16px;
    margin-left: 8px;
    margin-bottom: 4px;
    animation: fade-in 0.5s ease-out both;
}

/* ── 9. Pulsing Live Indicator ── */
.live-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    color: #4ade80;
    margin-bottom: 0.3rem;
}
.live-dot {
    width: 8px;
    height: 8px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
    animation: pulse-dot 1.5s ease-in-out infinite;
}
</style>
"""

FLOATING_SYMBOLS_HTML = """
<div class="floating-symbols">
    <span>&yen;</span><span>$</span><span>📈</span><span>📉</span><span>💹</span>
    <span>&yen;</span><span>📊</span><span>$</span><span>💱</span><span>📉</span>
</div>
"""

TICKER_ITEMS = [
    "¥161→142 (ugh)",
    "TOPIX -12% (ouch)",
    "VIX >60 (excuse me??)",
    "Nikkei -12.4% (yikes)",
    "$4T Unwind (not a typo)",
    "BOJ Rate 0.25% (finally)",
    "Black Monday Aug 5 (RIP portfolios)",
    "Transfer Entropy (the real MVP)",
    "Correlation could never",
]

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

        st.header("📚 What's This About?")
        st.markdown(
            "**Case 5 — Japan Carry Trade Unwind (2024)**\n\n"
            "The story of how a 17-year-old free money glitch finally got "
            "patched, markets threw a tantrum, and transfer entropy said "
            "'*I told you so.*' \n\n"
            "Spoiler: it gets dramatic."
        )

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

        # Did You Know? box
        if "fun_fact" not in st.session_state:
            st.session_state.fun_fact = random.choice(DID_YOU_KNOW_FACTS)
        st.info(f"🎲 **No Because Did You Know??**\n\n{st.session_state.fun_fact}")

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
        st.subheader("❓ Don't Know What to Ask? Try These")
        for emoji, q in EXAMPLE_QUESTIONS:
            if st.button(f"{emoji} {q}", key=q, use_container_width=True):
                st.session_state["prefill_question"] = q

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
        st.subheader("⚙️ Nerd Settings")
        model = st.selectbox(
            "Model",
            ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"],
            index=0,
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

        # Clear chat button
        if st.button("🗑️ Nuke the Chat (start fresh)", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("welcomed", None)
            st.session_state.pop("first_question_asked", None)
            st.rerun()

        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
        st.caption(
            "🎓 MGMT 69000 · Mastering AI for Finance · **Purdue University**\n\n"
            "*no portfolios were harmed in the making of this app (just feelings)*"
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

    # Inject custom CSS + floating symbols
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(FLOATING_SYMBOLS_HTML, unsafe_allow_html=True)

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
        '<div class="hero-caption">your slightly unhinged but very accurate finance bestie</div>',
        unsafe_allow_html=True,
    )

    # ── Ticker Tape Banner ──
    ticker_text = " | ".join(TICKER_ITEMS)
    doubled = f"{ticker_text}  |||  {ticker_text}"
    st.markdown(
        f'<div class="ticker-wrap">'
        f'<div class="ticker-content"><span>{doubled}</span></div></div>',
        unsafe_allow_html=True,
    )

    # ── Key Stats Dashboard ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📉 Topix (yikes)", value="-12%", delta="Aug 5")
    with col2:
        st.metric(label="😱 VIX (ugh)", value=">60", delta="Panic mode")
    with col3:
        st.metric(label="💱 USD/JPY", value="161→142", delta="ouch")
    with col4:
        st.metric(label="🏦 BOJ Rate", value="0.25%", delta="finally lol")

    # ── Visual Timeline (staggered animation) ──
    with st.expander("📅 The Timeline of Chaos — How It All Went Down"):
        for i, (emoji, date, description) in enumerate(TIMELINE_EVENTS):
            delay = i * 0.15
            st.markdown(
                f'<div class="timeline-item" style="animation-delay:{delay}s">'
                f"<strong>{emoji} {date}</strong><br>{description}</div>",
                unsafe_allow_html=True,
            )

    # ── Contagion Flow Diagram ──
    with st.expander("🔗 The Domino Effect — Who Broke What (and When)"):
        flow_parts: list[str] = []
        for idx, step in enumerate(CONTAGION_FLOW_STEPS):
            flow_parts.append(
                f'<div class="contagion-step">'
                f'<div class="label">{step["label"]}</div>'
                f'<div class="detail">{step["detail"]}</div></div>'
            )
            if idx < len(CONTAGION_FLOW_STEPS) - 1:
                flow_parts.append('<div class="contagion-arrow">→</div>')
        st.markdown(
            f'<div class="contagion-flow">{"".join(flow_parts)}</div>',
            unsafe_allow_html=True,
        )
        # Second Lottie animation
        lottie_chart = load_lottie_url(LOTTIE_CHART_URL)
        if lottie_chart:
            st_lottie(lottie_chart, height=120, key="contagion_lottie")

    # Glowing divider instead of st.divider()
    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

    # Load case content and build system prompt
    case_content = load_case_content()
    system_prompt = build_system_prompt(case_content)
    settings = render_sidebar(case_content)

    # Initialize Gemini client (via OpenAI-compatible endpoint)
    api_key = st.secrets.get("GOOGLE_API_KEY", None)
    if not api_key:
        st.warning(
            "⚠️ Bestie, I can't talk without an API key. Pop your Google AI "
            "key into **Manage app → Settings → Secrets** like this:\n\n"
            '`GOOGLE_API_KEY = "your-key-here"`\n\n'
            "Get a free one at https://aistudio.google.com/apikey ☕"
        )
        st.stop()

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome message on first load
    if not st.session_state.get("welcomed"):
        st.session_state.welcomed = True
        welcome = (
            "👋 Hey bestie! I'm your **Japan Carry Trade expert** — think of me "
            "as that friend who actually reads the case *and* has opinions about "
            "it.\n\n"
            "Ask me anything about the 2024 yen carry trade unwind, the absolute "
            "chaos of Black Monday, how contagion spreads faster than gossip, or "
            "why transfer entropy is lowkey the most underrated tool in finance.\n\n"
            "💡 *Not sure where to start? The sidebar has some bangers. Go on, "
            "click one. I won't judge.*"
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome}
        )

    # Display chat history with custom avatars
    for msg in st.session_state.messages:
        avatar = "🧑‍🎓" if msg["role"] == "user" else "🏦"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Pulsing "Live" indicator above chat input
    st.markdown(
        '<div class="live-indicator">'
        '<span class="live-dot"></span> go ahead, ask me something spicy</div>',
        unsafe_allow_html=True,
    )

    # Handle prefilled question from sidebar button
    prefill = st.session_state.pop("prefill_question", None)
    prompt = st.chat_input("type something… I promise I won't roast you (much) 💬") or prefill

    if prompt:
        # Easter egg: balloons on first question — welcome to the party!
        if not st.session_state.get("first_question_asked"):
            st.session_state.first_question_asked = True
            st.balloons()
            st.toast("🎉 First question! Let's gooo", icon="✨")

        # Easter egg: snow for crash/Black Monday — pouring one out
        prompt_lower = prompt.lower()
        if "black monday" in prompt_lower or "crash" in prompt_lower:
            st.snow()
            st.toast("❄️ It's giving… financial winter", icon="💀")

        # Easter egg: toast reactions for fun keywords
        if "vix" in prompt_lower:
            st.toast("VIX above 60 is basically a scream", icon="😱")
        elif "correlation" in prompt_lower:
            st.toast("Correlation walked so transfer entropy could run", icon="🏃")
        elif "driver" in prompt_lower:
            st.toast("DRIVER framework activated — slay", icon="🧭")

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
            try:
                stream = client.chat.completions.create(
                    model=settings["model"],
                    messages=api_messages,
                    temperature=settings["temperature"],
                    stream=True,
                )
                response = st.write_stream(stream)
            except openai.AuthenticationError:
                response = (
                    "🔑 Yikes — Google rejected the API key. Check **Manage "
                    "app → Settings → Secrets** and make sure `GOOGLE_API_KEY` "
                    "is valid. Grab a free one at https://aistudio.google.com/apikey"
                )
                st.error(response)
            except openai.NotFoundError:
                response = (
                    f"🤔 The model **{settings['model']}** isn't available. "
                    "Try switching to **gemini-2.0-flash-lite** in the sidebar."
                )
                st.error(response)
            except openai.APIError as exc:
                response = (
                    f"💀 Gemini is being dramatic right now: {exc}\n\n"
                    "Try again in a sec?"
                )
                st.error(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )


if __name__ == "__main__":
    main()

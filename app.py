import streamlit as st
from openai import OpenAI
from pathlib import Path

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

--- CASE MATERIAL ---
{case_content}
--- END CASE MATERIAL ---
"""

EXAMPLE_QUESTIONS = [
    "What happened on August 5, 2024?",
    "How does transfer entropy differ from correlation?",
    "What is the contagion chain in the carry trade unwind?",
    "Why did correlation fail during the stress event?",
    "How does the DRIVER framework apply to this case?",
    "What is the Markov perspective on the BOJ policy shift?",
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


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def render_sidebar(case_content: str) -> dict:
    """Render sidebar with case overview, settings, and example questions."""
    with st.sidebar:
        st.header("About This Case")
        st.markdown(
            "**Case 5 — Japan Carry Trade Unwind (2024)**\n\n"
            "Explore the mechanics of the yen carry trade, the August 5 Black "
            "Monday crash, contagion mechanisms, and how transfer entropy "
            "reveals directional information flow in financial markets."
        )

        st.divider()
        st.subheader("Example Questions")
        for q in EXAMPLE_QUESTIONS:
            if st.button(q, key=q, use_container_width=True):
                st.session_state["prefill_question"] = q

        st.divider()
        st.subheader("Settings")
        model = st.selectbox(
            "Model",
            ["gpt-4.1", "gpt-4o-mini", "gpt-4.1-mini"],
            index=0,
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

        st.divider()
        st.caption(
            "MGMT 69000 · Mastering AI for Finance · Purdue University"
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

    st.title(APP_TITLE)
    st.caption("AI-powered Q&A grounded in the Japan Carry Trade case study")

    # Load case content and build system prompt
    case_content = load_case_content()
    system_prompt = build_system_prompt(case_content)
    settings = render_sidebar(case_content)

    # Initialize OpenAI client
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if not api_key:
        st.warning(
            "Please set your OpenAI API key in `.streamlit/secrets.toml` "
            "or as an environment variable `OPENAI_API_KEY`."
        )
        st.stop()

    client = OpenAI(api_key=api_key)

    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle prefilled question from sidebar button
    prefill = st.session_state.pop("prefill_question", None)
    prompt = st.chat_input("Ask about the Japan Carry Trade…") or prefill

    if prompt:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build messages for API call
        api_messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # Stream assistant response
        with st.chat_message("assistant"):
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

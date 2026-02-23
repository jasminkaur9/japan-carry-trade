"""Tests for the Japan Carry Trade Q&A app."""

from app import (
    CASE_DATA_PATH,
    CONTAGION_FLOW_STEPS,
    EXAMPLE_QUESTIONS,
    SYSTEM_PROMPT_TEMPLATE,
    TIMELINE_EVENTS,
    build_system_prompt,
    load_case_content,
)


def test_case_data_file_exists():
    """The case study markdown file must exist."""
    assert CASE_DATA_PATH.exists(), f"Missing case data at {CASE_DATA_PATH}"


def test_load_case_content_not_empty():
    """Case content should load and be non-empty."""
    content = load_case_content.__wrapped__()  # bypass st.cache_data
    assert len(content) > 500, "Case content appears too short"


def test_case_content_has_key_sections():
    """Case content should contain essential sections."""
    content = CASE_DATA_PATH.read_text(encoding="utf-8")
    for section in [
        "Background",
        "Timeline",
        "Key Data",
        "Contagion",
        "Transfer Entropy",
        "DRIVER",
    ]:
        assert section in content, f"Missing section: {section}"


def test_case_content_has_key_facts():
    """Case content should contain critical data points."""
    content = CASE_DATA_PATH.read_text(encoding="utf-8")
    for fact in ["12%", "VIX", "161", "142", "August 5"]:
        assert fact in content, f"Missing key fact: {fact}"


def test_build_system_prompt():
    """System prompt should incorporate case content."""
    prompt = build_system_prompt("TEST_CONTENT_HERE")
    assert "TEST_CONTENT_HERE" in prompt
    assert "Japan Carry Trade" in prompt
    assert "transfer entropy" in prompt.lower()


def test_system_prompt_template_has_placeholder():
    """Template must contain the {case_content} placeholder."""
    assert "{case_content}" in SYSTEM_PROMPT_TEMPLATE


def test_system_prompt_instructs_emoji_usage():
    """System prompt should tell the AI to use emojis."""
    assert "emoji" in SYSTEM_PROMPT_TEMPLATE.lower()


def test_example_questions_have_emojis():
    """Each example question should be a (emoji, question) tuple."""
    for item in EXAMPLE_QUESTIONS:
        assert isinstance(item, tuple) and len(item) == 2


def test_timeline_events_non_empty():
    """Timeline events should exist and have correct structure."""
    assert len(TIMELINE_EVENTS) > 0
    for item in TIMELINE_EVENTS:
        assert isinstance(item, tuple) and len(item) == 3


def test_contagion_flow_steps():
    """Contagion flow steps should exist with label and detail keys."""
    assert len(CONTAGION_FLOW_STEPS) >= 3
    for step in CONTAGION_FLOW_STEPS:
        assert "label" in step, "Each step needs a 'label' key"
        assert "detail" in step, "Each step needs a 'detail' key"

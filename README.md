# Japan Carry Trade Q&A

AI-powered chat interface grounded in the 2024 Japan Carry Trade case study for MGMT 69000: Mastering AI for Finance at Purdue University.

## Overview

Ask questions about the yen carry trade unwind, the August 5 Black Monday crash, transfer entropy analysis, and the contagion mechanism — and get answers grounded in the case material.

## Setup

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-your-key-here"
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
pytest test_app.py -v
```

## Architecture

- **`case_data/japan_carry_trade.md`** — Case study knowledge base
- **`app.py`** — Streamlit chat app with OpenAI integration
- **`.github/workflows/ci.yml`** — CI/CD pipeline (lint + test)

The case content (~7K tokens) is loaded directly into the system prompt — no vector DB needed.

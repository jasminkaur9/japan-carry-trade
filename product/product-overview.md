# Japan Carry Trade Q&A — Product Overview

## DRIVER Definition

### Discover
The 2024 Japan carry trade unwind was one of the most dramatic market events of the year. Students studying this case need an interactive way to explore the mechanics, timeline, and analytical frameworks (especially transfer entropy) involved in the crisis.

### Represent
An AI-powered chat interface grounded in the case study content. Users ask natural-language questions and receive answers that are faithful to the case material — covering the BOJ policy shift, the August 5 Black Monday event, contagion mechanisms, transfer entropy vs. correlation, and the DRIVER framework application.

### Implement
- Streamlit chat UI with OpenAI GPT integration
- Case study markdown loaded as system prompt context (simple RAG)
- Sidebar with case overview and example questions

### Validate
- Answers should be grounded in case content (no hallucination beyond case scope)
- Key facts verifiable: Topix -12%, VIX >60, USD/JPY 161→142, August 5 timeline

### Evolve
- Could extend to multi-case support across all MGMT 69000 cases
- Could add citation highlighting showing which part of the case informed each answer

### Reflect
- Simplest RAG approach (full context in system message) is appropriate given small case size (~7K tokens)
- No vector DB needed — avoids unnecessary complexity

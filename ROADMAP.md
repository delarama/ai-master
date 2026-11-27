# AI Master — Roadmap

A day-by-day path through practical AI engineering with the Claude API.
Each day adds one small, working, runnable script (`dayNN_<topic>.py`) plus a short
note in `notes/dayNN.md` covering what it shows and what I learned.

## Track 1 — API fundamentals
- [x] Day 01 — First message: system prompts & a negotiation persona (`day01_first_message.py`)
- [x] Day 02 — Streaming responses token-by-token
- [x] Day 03 — Multi-turn conversations (managing message history)
- [x] Day 04 — Temperature, max_tokens & stop sequences compared
- [x] Day 05 — Token counting & cost estimation
- [ ] Day 06 — Structured JSON output with validation
- [ ] Day 07 — Error handling, retries & rate limits

## Track 2 — Tools & agents
- [ ] Day 08 — Tool use: a single calculator tool
- [ ] Day 09 — Multiple tools & tool choice
- [ ] Day 10 — Tool Runner / agentic loop
- [ ] Day 11 — A small research agent with web-style tools (mocked)
- [ ] Day 12 — Vision: describing and extracting from images
- [ ] Day 13 — PDF / document input
- [ ] Day 14 — Prompt caching for long context

## Track 3 — Retrieval & evaluation
- [ ] Day 15 — Embeddings-free keyword retrieval over local notes
- [ ] Day 16 — Chunking strategies
- [ ] Day 17 — Simple RAG pipeline over this repo's notes
- [ ] Day 18 — LLM-as-judge eval harness
- [ ] Day 19 — Regression evals for prompts
- [ ] Day 20 — Prompt iteration log with measured results

## Track 4 — Shipping
- [ ] Day 21 — CLI wrapper with argparse
- [ ] Day 22 — FastAPI endpoint around a prompt
- [ ] Day 23 — Streaming over HTTP (SSE)
- [ ] Day 24 — Logging, tracing & usage dashboards
- [ ] Day 25 — Capstone: negotiation-coach agent combining tools, memory & evals

## Rules for daily work
- Everything must run (`python dayNN_*.py`) with only `ANTHROPIC_API_KEY` in `.env`.
- One logical change per commit; clear commit messages.
- Tests in `tests/` for anything that doesn't require a live API call.
- Changes land via pull request into `main`.

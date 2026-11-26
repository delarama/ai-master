# Day 02 — Streaming

**Script:** `day02_streaming.py`

## What it shows
- `client.messages.stream(...)` as a context manager yields text deltas via `stream.text_stream`.
- `stream.get_final_message()` still gives the full `Message`, including `usage`.
- Time-to-first-token (TTFT) is the latency a user actually *feels*; total time matters less for chat UX.

## Takeaways
- Stream whenever output goes to a human; it makes long replies feel instant.
- Streaming doesn't change token cost, only perceived latency.
- `flush=True` matters, otherwise the terminal buffers and the effect is lost.

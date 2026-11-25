# Day 01 — First message & system prompts

**Script:** `day1.py`

## What it shows
- Minimal `client.messages.create` call with a `system` prompt defining a persona.
- The system prompt holds a secret constraint (lowest price) the model should not reveal.
- `msg.usage` reports input/output tokens for cost tracking.

## Takeaways
- System prompts set role and hidden rules; user messages set the task.
- Keep API keys in `.env` (git-ignored) and load with `python-dotenv`.

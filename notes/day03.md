# Day 03 — Multi-turn conversations

**Script:** `day03_multiturn.py`

## What it shows
- The Messages API is **stateless**: each call resends the full history, so "memory" is just the list you send.
- `Conversation` enforces strict user → assistant alternation; the API rejects two same-role messages in a row.
- `window()` sends only the last N turns and always starts on a user message, which caps the cost of long chats.
- Replies are built from `text` blocks only, so other block types (like thinking) don't leak into history.

## Takeaways
- Input tokens grow every turn because the whole history is billed again; trimming or summarising is how you control cost.
- Dropping old turns means the model forgets them, so put anything that must persist (rules, persona) in the `system` prompt.
- Keep the full history locally even when you trim what you send; it's useful for logs and evals later.

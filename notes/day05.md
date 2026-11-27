# Day 05 — Token counting & cost estimation

**Script:** `day05_token_costs.py`

## What it shows
- `client.messages.count_tokens(...)` takes the same `model`/`system`/`messages` as `create` and returns `input_tokens` **without running the model**, so you can check size and cost before sending.
- Cost = input tokens × input rate + output tokens × output rate, priced per million tokens.
- After a real call, `response.usage` gives the exact `input_tokens` / `output_tokens` to price.

## Prices used (per million tokens, as of 2026-11-03)
| Model | Input | Output |
|---|---|---|
| claude-fable-5-2 | $8.00 | $40.00 |
| claude-opus-5-5 | $4.00 | $20.00 |
| claude-sonnet-5-5 | $2.00 | $10.00 |
| claude-haiku-5-5 | $0.10 | $0.50 (≤100K-token prompts) |

## Takeaways
- Output tokens cost 5× input on every current model, so long answers dominate the bill. Ask for brevity and set sensible `max_tokens`.
- You can only *count* input in advance; output has to be estimated, so budget with an assumed reply length.
- Multi-turn chats (Day 03) resend history, so input cost grows every turn; counting tokens shows exactly how fast.
- Prices change. Keep them in one table with a date, and check the pricing page before relying on them.

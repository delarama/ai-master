# Day 04 — Effort, max_tokens & stop sequences

**Script:** `day04_sampling_params.py`

## What it shows
- The same prompt run under four settings, printed as one table: variant, `stop_reason`, output tokens, text preview.
- **Effort** (`output_config={"effort": "low" | ... | "max"}`) controls how much the model thinks. Low is faster and cheaper; high is more thorough.
- `max_tokens` is a hard cap that includes thinking: the reply is cut off (or empty) and `stop_reason` becomes `"max_tokens"`.
- `stop_sequences` end generation early; `stop_reason` is `"stop_sequence"` and the matched text is **not** included.

## Correction: temperature is gone
The first version of this day compared `temperature` 0.0 vs 1.0. Current Claude models removed
`temperature`/`top_p`/`top_k` (requests that set them are rejected), and the installed SDK no longer
accepts the argument at all. The mocked tests didn't catch it because a mock accepts any keyword, so
there's now a test that checks request settings against the real SDK signature.

## Takeaways
- Always check `stop_reason` before trusting output. `"max_tokens"` means the answer is incomplete.
- Tune effort per task: `low` for chat, classification and simple extraction; `high` or above for hard reasoning.
- Stop sequences are a cheap way to bound output (e.g. stop at `"</answer>"`) and save tokens.
- Mocks only prove your code calls *something*. Pair them with a check against the real SDK.

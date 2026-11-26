# Day 04 — Temperature, max_tokens & stop sequences

**Script:** `day04_sampling_params.py`

## What it shows
- The same prompt run under four settings, printed as one table: variant, `stop_reason`, output tokens, text preview.
- `temperature` changes wording, not instructions: at 0.0 reruns are near-identical; at 1.0 phrasing varies between runs.
- `max_tokens` is a hard cap: the reply is cut mid-sentence and `stop_reason` becomes `"max_tokens"`.
- `stop_sequences` end generation early; `stop_reason` is `"stop_sequence"` and the matched text is **not** included in the output.

## Takeaways
- Always check `stop_reason` before trusting output. `"max_tokens"` means the answer is incomplete.
- Use low temperature for extraction, classification and tests; higher for brainstorming and copy.
- Stop sequences are a cheap way to bound output (e.g. stop at `"</answer>"`) and save tokens.
- `max_tokens` only limits output; it doesn't make answers more concise, so ask for brevity in the prompt.

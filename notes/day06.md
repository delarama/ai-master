# Day 06 — Structured JSON output with validation

**Script:** `day06_structured_output.py`

## What it shows
- Define the output you want as a **Pydantic model** (`CarListing`), with field descriptions as hints.
- `client.messages.parse(..., output_format=CarListing)` turns the model into a JSON schema, sends it as `output_config.format`, and the reply is **constrained** to match it, so there's no "please return JSON" prompting and no fragile `json.loads` on free text.
- `response.parsed_output` is already a `CarListing`; it's `None` if nothing parsed (e.g. a refusal), so check it.
- `int | None` makes a field nullable but still required: the model must say "not stated" explicitly.
- `check_listing()` adds rules a schema can't express (sane year range, positive price).

## Takeaways
- Schema-valid ≠ correct. The schema guarantees shape and types; business rules and facts still need checking.
- Use field descriptions for units and conventions ("whole US dollars"), since they become part of the schema the model sees.
- Without the SDK helper, pass a raw schema dict as `output_config={"format": {"type": "json_schema", "schema": ...}}`.
- Structured output is the right tool when code consumes the answer; free text is for humans.

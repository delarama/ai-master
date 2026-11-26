"""Day 04 — Temperature, max_tokens & stop sequences compared.

Sends the same prompt with different generation settings and prints a table
showing how each one changes the output, the stop reason and the token count.

- temperature: 0.0 is close to deterministic; 1.0 gives more varied wording.
- max_tokens: a hard cap. When hit, stop_reason is "max_tokens" and the text is cut off.
- stop_sequences: generation halts when the model emits one; stop_reason is "stop_sequence".
"""

from dataclasses import dataclass, field
from typing import Any

import anthropic

from common import DEFAULT_MODEL, friendly_api_errors, make_client, response_text

PROMPT = (
    "Write a three-line sales pitch for a used 2018 Honda Civic. "
    "Number the lines 1., 2., 3. and end with the word DONE."
)


@dataclass(frozen=True)
class Variant:
    """One set of generation settings to try."""

    label: str
    temperature: float = 1.0
    max_tokens: int = 300
    stop_sequences: list[str] = field(default_factory=list)

    def request_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": DEFAULT_MODEL,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self.stop_sequences:
            kwargs["stop_sequences"] = self.stop_sequences
        return kwargs


VARIANTS = [
    Variant("temperature 0.0", temperature=0.0),
    Variant("temperature 1.0", temperature=1.0),
    Variant("max_tokens 20", temperature=0.0, max_tokens=20),
    Variant('stop at "3."', temperature=0.0, stop_sequences=["3."]),
]


@dataclass(frozen=True)
class Row:
    label: str
    stop_reason: str
    output_tokens: int
    text: str


def run_variant(client: anthropic.Anthropic, variant: Variant, prompt: str = PROMPT) -> Row:
    """Call the API with one variant's settings and summarise the result."""
    response = client.messages.create(
        messages=[{"role": "user", "content": prompt}], **variant.request_kwargs()
    )
    text = response_text(response)
    return Row(variant.label, response.stop_reason, response.usage.output_tokens, text)


def preview(text: str, width: int = 60) -> str:
    """Collapse whitespace and truncate so each result fits on one table line."""
    flat = " ".join(text.split())
    return flat if len(flat) <= width else flat[: width - 1] + "…"


def format_table(rows: list[Row]) -> str:
    header = f"{'variant':<18} {'stop_reason':<14} {'tokens':>6}  output"
    lines = [header, "-" * len(header)]
    for row in rows:
        lines.append(
            f"{row.label:<18} {row.stop_reason:<14} {row.output_tokens:>6}  {preview(row.text)}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    with friendly_api_errors():
        client = make_client()
        print(format_table([run_variant(client, v) for v in VARIANTS]))

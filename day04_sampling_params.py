"""Day 04 — Effort, max_tokens & stop sequences compared.

Sends the same prompt with different generation settings and prints a table
showing how each one changes the output, the stop reason and the token count.

- effort (`output_config={"effort": ...}`): how much the model thinks before
  answering. Low is faster and cheaper; high is more thorough. Current Claude
  models removed `temperature`/`top_p`, so effort is the main quality/cost dial.
- max_tokens: a hard cap on output, thinking included. When hit, stop_reason is
  "max_tokens" and the text is cut off (or empty if thinking used it all).
- stop_sequences: generation halts when the model emits one; stop_reason is "stop_sequence".
"""

from dataclasses import dataclass, field
from typing import Any, Literal

import anthropic

from common import DEFAULT_MODEL, friendly_api_errors, make_client, response_text

Effort = Literal["low", "medium", "high", "xhigh", "max"]

PROMPT = (
    "Write a three-line sales pitch for a used 2018 Honda Civic. "
    "Number the lines 1., 2., 3. and end with the word DONE."
)


@dataclass(frozen=True)
class Variant:
    """One set of generation settings to try."""

    label: str
    effort: Effort | None = None  # None = the model's default
    max_tokens: int = 2000
    stop_sequences: list[str] = field(default_factory=list)

    def request_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"model": DEFAULT_MODEL, "max_tokens": self.max_tokens}
        if self.effort:
            kwargs["output_config"] = {"effort": self.effort}
        if self.stop_sequences:
            kwargs["stop_sequences"] = self.stop_sequences
        return kwargs


VARIANTS = [
    Variant("effort low", effort="low"),
    Variant("effort high", effort="high"),
    Variant("max_tokens 40", effort="low", max_tokens=40),
    Variant('stop at "3."', effort="low", stop_sequences=["3."]),
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

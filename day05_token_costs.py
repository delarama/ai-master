"""Day 05 — Token counting & cost estimation.

Counts the input tokens of a request *before* sending it (free, via
`messages.count_tokens`), estimates what it would cost on each current model,
then sends it once and prices the real usage reported in the response.

Prices change: the table below is a dated snapshot, so check
https://claude.com/pricing before relying on it for budgeting.
"""

from dataclasses import dataclass

import anthropic

from common import (
    BUYER_OPENING,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    SELLER_SYSTEM_PROMPT,
    friendly_api_errors,
    make_client,
)

PRICES_AS_OF = "2026-11-03"


@dataclass(frozen=True)
class Price:
    """US dollars per million tokens."""

    input: float
    output: float


# Standard first-party API rates (no caching, batch or fast-mode discounts/premiums).
PRICES: dict[str, Price] = {
    "claude-fable-5-2": Price(8.00, 40.00),
    "claude-opus-5-5": Price(4.00, 20.00),
    "claude-sonnet-5-5": Price(2.00, 10.00),
    "claude-haiku-5-5": Price(0.10, 0.50),  # prompts up to 100K tokens
}


def cost_usd(model: str, input_tokens: int, output_tokens: int = 0) -> float:
    """Dollar cost of a request with the given token counts on `model`."""
    try:
        price = PRICES[model]
    except KeyError:
        raise ValueError(f"No price on file for {model!r}; add it to PRICES.") from None
    return (input_tokens * price.input + output_tokens * price.output) / 1_000_000


def format_usd(amount: float) -> str:
    """Show tiny amounts readably: $0.000123 rather than $0.00."""
    return f"${amount:.6f}" if amount < 0.01 else f"${amount:.4f}"


def count_input_tokens(client: anthropic.Anthropic, model: str, system: str, user: str) -> int:
    """Input tokens the request would use, without running the model."""
    result = client.messages.count_tokens(
        model=model,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return result.input_tokens


def estimate_table(input_tokens: int, assumed_output_tokens: int) -> str:
    """One line per model: estimated cost for the same token counts."""
    lines = [f"{'model':<20} {'est. cost':>12}   (as of {PRICES_AS_OF})"]
    for model in PRICES:
        lines.append(
            f"{model:<20} {format_usd(cost_usd(model, input_tokens, assumed_output_tokens)):>12}"
        )
    return "\n".join(lines)


def describe_actual_cost(model: str, usage: anthropic.types.Usage) -> str:
    """One line pricing the real token usage reported by a response."""
    actual = cost_usd(model, usage.input_tokens, usage.output_tokens)
    return (
        f"Actual on {model}: {usage.input_tokens} in / "
        f"{usage.output_tokens} out = {format_usd(actual)}"
    )


if __name__ == "__main__":
    with friendly_api_errors():
        client = make_client()
        n_in = count_input_tokens(client, DEFAULT_MODEL, SELLER_SYSTEM_PROMPT, BUYER_OPENING)
        print(f"Input tokens (counted before sending): {n_in}")
        print("\nEstimate assuming a 200-token reply:")
        print(estimate_table(n_in, assumed_output_tokens=200))

        response = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            system=SELLER_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": BUYER_OPENING}],
        )
        print("\n" + describe_actual_cost(DEFAULT_MODEL, response.usage))

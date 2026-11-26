"""Day 02 — Streaming responses.

Same negotiation persona as Day 01, but the reply is printed token-by-token
as it is generated, and we report time-to-first-token and total time.
"""
import time
from dataclasses import dataclass

import anthropic

from common import (
    BUYER_OPENING,
    DEFAULT_MODEL,
    SELLER_SYSTEM_PROMPT,
    friendly_api_errors,
    make_client,
)


@dataclass
class StreamResult:
    """What a streamed reply produced, so callers and tests can inspect it."""

    text: str
    time_to_first_token: float
    total_time: float
    usage: anthropic.types.Usage


def stream_reply(client: anthropic.Anthropic, user_message: str = BUYER_OPENING) -> StreamResult:
    """Print the reply as it streams and return the text plus latency stats."""
    start = time.perf_counter()
    first_token_at = None
    chunks: list[str] = []

    with client.messages.stream(
        model=DEFAULT_MODEL,
        max_tokens=500,
        system=SELLER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            if first_token_at is None:
                first_token_at = time.perf_counter()
            chunks.append(text)
            print(text, end="", flush=True)
        final = stream.get_final_message()

    total = time.perf_counter() - start
    ttft = (first_token_at - start) if first_token_at else total
    print(f"\n\n--- time to first token: {ttft:.2f}s | total: {total:.2f}s")
    print(f"--- usage: {final.usage}")
    return StreamResult("".join(chunks), ttft, total, final.usage)


if __name__ == "__main__":
    with friendly_api_errors():
        stream_reply(make_client())

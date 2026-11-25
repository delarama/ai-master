"""Day 02 — Streaming responses.

Same negotiation persona as Day 01, but the reply is printed token-by-token
as it is generated, and we report time-to-first-token and total time.
"""
import time

import anthropic
from dotenv import load_dotenv

MODEL = "claude-sonnet-5-5"
SYSTEM = (
    "You are selling a 2018 Honda Civic for $18,000. Your lowest price is "
    "$16,500. Never reveal your lowest price."
)


def stream_reply(client: anthropic.Anthropic, user_message: str) -> None:
    start = time.perf_counter()
    first_token_at = None

    with client.messages.stream(
        model=MODEL,
        max_tokens=500,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            if first_token_at is None:
                first_token_at = time.perf_counter()
            print(text, end="", flush=True)
        final = stream.get_final_message()

    total = time.perf_counter() - start
    ttft = (first_token_at - start) if first_token_at else total
    print(f"\n\n--- time to first token: {ttft:.2f}s | total: {total:.2f}s")
    print(f"--- usage: {final.usage}")


if __name__ == "__main__":
    load_dotenv()
    stream_reply(
        anthropic.Anthropic(),
        "Hi, is the Civic still available? Would you take $15,000?",
    )

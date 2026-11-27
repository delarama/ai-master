"""Day 01 — First message & system prompts.

Sends one message to Claude with a system prompt that defines a car-seller
persona holding a secret (their lowest price), then prints the reply and usage.
"""

import anthropic

from common import (
    BUYER_OPENING,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    SELLER_SYSTEM_PROMPT,
    friendly_api_errors,
    make_client,
    response_text,
)


def negotiate(
    client: anthropic.Anthropic, user_message: str = BUYER_OPENING
) -> anthropic.types.Message:
    """Send a single buyer message to the seller persona and return the full Message."""
    return client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=DEFAULT_MAX_TOKENS,
        system=SELLER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )


if __name__ == "__main__":
    with friendly_api_errors():
        msg = negotiate(make_client())
        print(response_text(msg))
        print(msg.usage)

"""Day 01 — First message & system prompts.

Sends one message to Claude with a system prompt that defines a car-seller
persona holding a secret (their lowest price), then prints the reply and usage.
"""

import anthropic

from common import BUYER_OPENING, DEFAULT_MODEL, SELLER_SYSTEM_PROMPT, make_client


def negotiate(client: anthropic.Anthropic, user_message: str = BUYER_OPENING) -> anthropic.types.Message:
    """Send a single buyer message to the seller persona and return the full Message."""
    return client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=500,
        system=SELLER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )


if __name__ == "__main__":
    msg = negotiate(make_client())
    print(msg.content[0].text)
    print(msg.usage)

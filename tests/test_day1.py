from unittest.mock import MagicMock

import day1
from common import BUYER_OPENING, DEFAULT_MODEL, SELLER_SYSTEM_PROMPT


def test_negotiate_sends_persona_and_buyer_message():
    client = MagicMock()
    client.messages.create.return_value = "reply"

    assert day1.negotiate(client) == "reply"

    kwargs = client.messages.create.call_args.kwargs
    assert kwargs["model"] == DEFAULT_MODEL
    assert kwargs["system"] == SELLER_SYSTEM_PROMPT
    assert kwargs["messages"] == [{"role": "user", "content": BUYER_OPENING}]


def test_negotiate_accepts_custom_message():
    client = MagicMock()
    day1.negotiate(client, "Final offer: $16,000")
    assert client.messages.create.call_args.kwargs["messages"][0]["content"] == (
        "Final offer: $16,000"
    )


def test_seller_prompt_keeps_floor_price_secret():
    assert "Never reveal your lowest price" in SELLER_SYSTEM_PROMPT

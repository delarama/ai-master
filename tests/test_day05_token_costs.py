from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from day05_token_costs import (
    PRICES,
    cost_usd,
    count_input_tokens,
    estimate_table,
    format_usd,
)


def test_cost_usd_combines_input_and_output_rates():
    # Sonnet 5.5: $2 in / $10 out per million tokens
    assert cost_usd("claude-sonnet-5-5", 1_000_000, 1_000_000) == pytest.approx(12.0)
    assert cost_usd("claude-sonnet-5-5", 500, 0) == pytest.approx(0.001)


def test_cost_usd_rejects_unknown_model():
    with pytest.raises(ValueError, match="No price on file"):
        cost_usd("claude-made-up", 10)


def test_output_tokens_cost_more_than_input_for_every_model():
    for price in PRICES.values():
        assert price.output > price.input


def test_format_usd_keeps_small_amounts_visible():
    assert format_usd(0.000123) == "$0.000123"
    assert format_usd(1.5) == "$1.5000"


def test_count_input_tokens_sends_system_and_user_message():
    client = MagicMock()
    client.messages.count_tokens.return_value = SimpleNamespace(input_tokens=42)

    assert count_input_tokens(client, "claude-sonnet-5-5", "sys", "hello") == 42

    kwargs = client.messages.count_tokens.call_args.kwargs
    assert kwargs == {
        "model": "claude-sonnet-5-5",
        "system": "sys",
        "messages": [{"role": "user", "content": "hello"}],
    }


def test_estimate_table_lists_every_priced_model():
    table = estimate_table(input_tokens=100, assumed_output_tokens=200)
    for model in PRICES:
        assert model in table
    assert len(table.splitlines()) == len(PRICES) + 1

import inspect
from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from anthropic.resources.messages import Messages
from pydantic import ValidationError

from day06_structured_output import CarListing, check_listing, extract_listing

GOOD = CarListing(
    make="Honda",
    model="Civic",
    year=2018,
    price_usd=18000,
    mileage_km=92000,
    features=["sunroof"],
    red_flags=["dent"],
)


def test_extract_listing_passes_model_as_output_format_and_returns_parsed():
    client = MagicMock()
    client.messages.parse.return_value = SimpleNamespace(parsed_output=GOOD, stop_reason="end_turn")

    assert extract_listing(client, "ad text") == GOOD

    kwargs = client.messages.parse.call_args.kwargs
    assert kwargs["output_format"] is CarListing
    assert kwargs["messages"] == [{"role": "user", "content": "ad text"}]


def test_extract_listing_raises_when_nothing_parsed():
    client = MagicMock()
    client.messages.parse.return_value = SimpleNamespace(parsed_output=None, stop_reason="refusal")
    with pytest.raises(ValueError, match="stop_reason=refusal"):
        extract_listing(client, "ad text")


def test_parse_call_matches_real_sdk_signature():
    accepted = set(inspect.signature(Messages.parse).parameters)
    assert {"model", "max_tokens", "system", "messages", "output_format"} <= accepted


def test_schema_rejects_wrong_types():
    with pytest.raises(ValidationError):
        CarListing.model_validate({**GOOD.model_dump(), "year": "twenty eighteen"})


def test_schema_marks_mileage_nullable_and_all_fields_required():
    schema = CarListing.model_json_schema()
    assert set(schema["required"]) == set(CarListing.model_fields)
    assert {"type": "null"} in schema["properties"]["mileage_km"]["anyOf"]


def test_check_listing_accepts_sane_listing():
    assert check_listing(GOOD, today=date(2026, 11, 28)) == []


def test_check_listing_flags_impossible_values():
    bad = GOOD.model_copy(update={"year": 2031, "price_usd": 0, "mileage_km": -5})
    problems = check_listing(bad, today=date(2026, 11, 28))
    assert len(problems) == 3
    assert any("year 2031" in p for p in problems)

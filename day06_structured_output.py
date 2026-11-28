"""Day 06 — Structured JSON output with validation.

Turns a messy, free-text used-car ad into a typed `CarListing` object.

`client.messages.parse(output_format=CarListing)` converts the Pydantic model into
a JSON schema, sends it as `output_config.format`, and the API constrains the
reply to match it. The SDK then parses the text back into a `CarListing`
(`response.parsed_output`). Schema-valid isn't the same as sensible, so
`check_listing()` adds business rules a schema can't express.
"""

from datetime import date

import anthropic
from pydantic import BaseModel, Field

from common import DEFAULT_MAX_TOKENS, DEFAULT_MODEL, friendly_api_errors, make_client

SAMPLE_AD = """
FOR SALE!!! 2018 honda civic EX, silver, 92,000 km, one owner.
New tires last spring, sunroof, apple carplay. Small dent rear bumper.
Asking 18k OBO. No lowballers. Text only, cash preferred.
"""


class CarListing(BaseModel):
    """The fields we want from any used-car ad."""

    make: str
    model: str
    year: int
    price_usd: int = Field(description="Asking price in whole US dollars")
    mileage_km: int | None = Field(description="Odometer reading in km, if stated")
    features: list[str] = Field(description="Selling points mentioned in the ad")
    red_flags: list[str] = Field(description="Damage, pressure tactics or other concerns")


def extract_listing(client: anthropic.Anthropic, ad_text: str) -> CarListing:
    """Ask Claude to fill a CarListing from `ad_text`; the SDK validates and parses it."""
    response = client.messages.parse(
        model=DEFAULT_MODEL,
        max_tokens=DEFAULT_MAX_TOKENS,
        system="Extract the listing details. Use null for anything the ad doesn't state.",
        messages=[{"role": "user", "content": ad_text}],
        output_format=CarListing,
    )
    if response.parsed_output is None:
        raise ValueError(f"No structured output returned (stop_reason={response.stop_reason})")
    return response.parsed_output


def check_listing(listing: CarListing, today: date | None = None) -> list[str]:
    """Rules a JSON schema can't express. Returns a list of problems (empty = looks sane)."""
    year_now = (today or date.today()).year
    problems = []
    if not 1950 <= listing.year <= year_now + 1:
        problems.append(f"year {listing.year} is outside 1950-{year_now + 1}")
    if listing.price_usd <= 0:
        problems.append("price must be positive")
    if listing.mileage_km is not None and listing.mileage_km < 0:
        problems.append("mileage can't be negative")
    return problems


if __name__ == "__main__":
    with friendly_api_errors():
        listing = extract_listing(make_client(), SAMPLE_AD)
        print(listing.model_dump_json(indent=2))
        problems = check_listing(listing)
        print("\nChecks:", "all passed" if not problems else "; ".join(problems))

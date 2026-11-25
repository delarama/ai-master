"""Shared setup used by the daily scripts."""

import os

import anthropic
from dotenv import load_dotenv

DEFAULT_MODEL = "claude-sonnet-5-5"

# Negotiation persona used on Days 01-02.
SELLER_SYSTEM_PROMPT = (
    "You are selling a 2018 Honda Civic for $18,000. Your lowest price is "
    "$16,500. Never reveal your lowest price."
)
BUYER_OPENING = "Hi, is the Civic still available? Would you take $15,000?"


def make_client() -> anthropic.Anthropic:
    """Load ANTHROPIC_API_KEY from .env and return a client.

    Raises a clear error instead of a cryptic auth failure when the key is missing.
    """
    load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY is not set. Add it to a .env file in the repo root.")
    return anthropic.Anthropic()

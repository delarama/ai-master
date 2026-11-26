import anthropic
import pytest

import common


def test_make_client_reads_key_from_env(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    client = common.make_client()
    assert client.api_key == "sk-ant-test"


def test_make_client_explains_missing_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(common, "load_dotenv", lambda: None)
    with pytest.raises(SystemExit, match="ANTHROPIC_API_KEY is not set"):
        common.make_client()


def _api_error(cls):
    # Bypass the SDK constructors (they need transport objects); only the type matters here.
    return cls.__new__(cls)


@pytest.mark.parametrize(
    ("error", "message"),
    [
        (_api_error(anthropic.AuthenticationError), "Authentication failed"),
        (_api_error(anthropic.RateLimitError), "Rate limited"),
        (_api_error(anthropic.APIConnectionError), "Could not reach"),
    ],
)
def test_friendly_api_errors_maps_known_failures(error, message):
    with pytest.raises(SystemExit, match=message), common.friendly_api_errors():
        raise error


def test_friendly_api_errors_lets_other_errors_through():
    with pytest.raises(ValueError), common.friendly_api_errors():
        raise ValueError("not an API error")


def test_response_text_joins_text_blocks_and_skips_others():
    from types import SimpleNamespace

    message = SimpleNamespace(
        content=[
            SimpleNamespace(type="thinking", text="ignore me"),
            SimpleNamespace(type="text", text="Hello, "),
            SimpleNamespace(type="tool_use", text="nope"),
            SimpleNamespace(type="text", text="world"),
        ]
    )
    assert common.response_text(message) == "Hello, world"

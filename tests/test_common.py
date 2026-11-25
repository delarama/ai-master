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

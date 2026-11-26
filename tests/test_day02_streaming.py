from unittest.mock import MagicMock

import day02_streaming


def _fake_client(chunks, usage="usage"):
    stream = MagicMock()
    stream.text_stream = iter(chunks)
    stream.get_final_message.return_value = MagicMock(usage=usage)

    ctx = MagicMock()
    ctx.__enter__.return_value = stream
    ctx.__exit__.return_value = False

    client = MagicMock()
    client.messages.stream.return_value = ctx
    return client


def test_stream_reply_joins_chunks_and_reports_usage(capsys):
    client = _fake_client(["Yes, ", "it's ", "available."], usage="u")

    result = day02_streaming.stream_reply(client, "Is it available?")

    assert result.text == "Yes, it's available."
    assert result.usage == "u"
    assert 0 <= result.time_to_first_token <= result.total_time
    out = capsys.readouterr().out
    assert out.startswith("Yes, it's available.")
    assert "time to first token" in out


def test_stream_reply_handles_empty_stream():
    result = day02_streaming.stream_reply(_fake_client([]), "hi")
    assert result.text == ""
    assert result.time_to_first_token == result.total_time

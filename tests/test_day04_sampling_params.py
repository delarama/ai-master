from types import SimpleNamespace
from unittest.mock import MagicMock

from common import DEFAULT_MODEL
from day04_sampling_params import VARIANTS, Row, Variant, format_table, preview, run_variant


def _response(text, stop_reason="end_turn", output_tokens=12):
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason,
        usage=SimpleNamespace(output_tokens=output_tokens),
    )


def test_request_kwargs_omit_stop_sequences_when_unset():
    kwargs = Variant("plain", temperature=0.2, max_tokens=50).request_kwargs()
    assert kwargs == {"model": DEFAULT_MODEL, "temperature": 0.2, "max_tokens": 50}


def test_request_kwargs_include_stop_sequences_when_set():
    kwargs = Variant("stop", stop_sequences=["3."]).request_kwargs()
    assert kwargs["stop_sequences"] == ["3."]


def test_variants_cover_each_parameter():
    assert {v.temperature for v in VARIANTS} >= {0.0, 1.0}
    assert any(v.max_tokens < 50 for v in VARIANTS)
    assert any(v.stop_sequences for v in VARIANTS)


def test_run_variant_passes_settings_and_summarises():
    client = MagicMock()
    client.messages.create.return_value = _response("1. Reliable", "stop_sequence", 5)
    variant = Variant("stop", temperature=0.0, stop_sequences=["2."])

    row = run_variant(client, variant, prompt="pitch it")

    kwargs = client.messages.create.call_args.kwargs
    assert kwargs["messages"] == [{"role": "user", "content": "pitch it"}]
    assert kwargs["stop_sequences"] == ["2."]
    assert kwargs["temperature"] == 0.0
    assert row == Row("stop", "stop_sequence", 5, "1. Reliable")


def test_preview_flattens_and_truncates():
    assert preview("a\n  b\tc") == "a b c"
    long = preview("x" * 100, width=10)
    assert len(long) == 10 and long.endswith("…")


def test_format_table_has_one_line_per_row():
    rows = [Row("t0", "end_turn", 30, "hello\nworld"), Row("cap", "max_tokens", 20, "")]
    table = format_table(rows)
    lines = table.splitlines()
    assert len(lines) == 4
    assert "hello world" in lines[2]
    assert "max_tokens" in lines[3]

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from day03_multiturn import Conversation, ask, chat_loop


def _reply(text):
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])


def test_alternation_is_enforced():
    convo = Conversation(system="s")
    with pytest.raises(ValueError):
        convo.add_assistant("no user yet")
    convo.add_user("hi")
    with pytest.raises(ValueError):
        convo.add_user("hi again")


def test_window_keeps_last_turns_and_starts_with_user():
    convo = Conversation(system="s", max_turns=2)
    for i in range(4):
        convo.add_user(f"u{i}")
        convo.add_assistant(f"a{i}")
    convo.add_user("u4")

    window = convo.window()
    assert [m["content"] for m in window] == ["u3", "a3", "u4"]
    assert window[0]["role"] == "user"
    assert len(convo.messages) == 9  # full history is kept; only the window is trimmed


def test_ask_sends_full_window_and_records_reply():
    client = MagicMock()
    client.messages.create.side_effect = [_reply("No, $17,500."), _reply("$17,000 is my best.")]
    convo = Conversation(system="seller")

    assert ask(client, convo, "$15,000?") == "No, $17,500."
    assert ask(client, convo, "$16,000?") == "$17,000 is my best."

    second_call = client.messages.create.call_args_list[1].kwargs
    assert second_call["system"] == "seller"
    sent = [m["content"] for m in second_call["messages"]]
    assert sent == ["$15,000?", "No, $17,500.", "$16,000?"]
    assert convo.messages[-1] == {"role": "assistant", "content": "$17,000 is my best."}


def test_ask_ignores_non_text_blocks():
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[
            SimpleNamespace(type="thinking", text="hmm"),
            SimpleNamespace(type="text", text="ok"),
        ]
    )
    assert ask(client, Conversation(system="s"), "hi") == "ok"


def test_chat_loop_stops_on_empty_line(monkeypatch, capsys):
    inputs = iter(["$15,000?", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    client = MagicMock()
    client.messages.create.return_value = _reply("Counter: $17,500")

    chat_loop(client, Conversation(system="s"))

    assert "seller> Counter: $17,500" in capsys.readouterr().out
    assert client.messages.create.call_count == 1


def test_max_turns_must_be_positive():
    with pytest.raises(ValueError):
        Conversation(system="s", max_turns=0)


def test_window_with_one_turn_sends_only_pending_message():
    convo = Conversation(system="s", max_turns=1)
    convo.add_user("u0")
    convo.add_assistant("a0")
    convo.add_user("u1")
    assert [m["content"] for m in convo.window()] == ["u1"]


def test_chat_loop_stops_on_eof(monkeypatch):
    def raise_eof(_):
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)
    client = MagicMock()
    chat_loop(client, Conversation(system="s"))
    client.messages.create.assert_not_called()


def test_ask_rolls_back_turn_when_reply_is_empty():
    client = MagicMock()
    client.messages.create.side_effect = [
        SimpleNamespace(content=[], stop_reason="refusal"),
        _reply("Sure, $17,000."),
    ]
    convo = Conversation(system="s")

    note = ask(client, convo, "something declined")
    assert "stop_reason=refusal" in note
    assert convo.messages == []  # nothing invalid left behind

    assert ask(client, convo, "$16,000?") == "Sure, $17,000."
    assert [m["role"] for m in convo.messages] == ["user", "assistant"]

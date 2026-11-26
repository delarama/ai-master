"""Day 03 — Multi-turn conversations.

The Messages API is stateless: every call must resend the whole conversation.
This script keeps the history in a small `Conversation` class, lets you haggle
with the Day 01 seller over several turns, and trims old turns so long chats
stay within a token budget.

Run it and type offers; enter an empty line (or Ctrl-D) to stop.
"""

from dataclasses import dataclass, field

import anthropic

from common import (
    DEFAULT_MODEL,
    SELLER_SYSTEM_PROMPT,
    friendly_api_errors,
    make_client,
    response_text,
)

Message = dict[str, str]


@dataclass
class Conversation:
    """Message history for one chat, kept in the strict user/assistant order the API needs."""

    system: str
    max_turns: int = 10  # one turn = one user message + one assistant reply
    messages: list[Message] = field(default_factory=list)

    def add_user(self, text: str) -> None:
        if self.messages and self.messages[-1]["role"] == "user":
            raise ValueError("Two user messages in a row; add the assistant reply first.")
        self.messages.append({"role": "user", "content": text})

    def add_assistant(self, text: str) -> None:
        if not self.messages or self.messages[-1]["role"] != "user":
            raise ValueError("An assistant reply must follow a user message.")
        self.messages.append({"role": "assistant", "content": text})

    def window(self) -> list[Message]:
        """The messages to send: the most recent `max_turns` turns, always starting with a user."""
        keep = self.max_turns * 2
        if self.messages and self.messages[-1]["role"] == "user":
            keep -= 1  # the pending user message counts toward the newest turn
        recent = self.messages[-keep:] if keep > 0 else []
        while recent and recent[0]["role"] != "user":
            recent = recent[1:]
        return recent


def ask(client: anthropic.Anthropic, convo: Conversation, text: str) -> str:
    """Send `text` as the next user turn, record the reply in history, and return it."""
    convo.add_user(text)
    response = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens=500,
        system=convo.system,
        messages=convo.window(),
    )
    reply = response_text(response)
    convo.add_assistant(reply)
    return reply


def chat_loop(client: anthropic.Anthropic, convo: Conversation) -> None:
    while True:
        try:
            text = input("\nyou> ").strip()
        except EOFError:
            break
        if not text:
            break
        print(f"seller> {ask(client, convo, text)}")


if __name__ == "__main__":
    with friendly_api_errors():
        chat_loop(make_client(), Conversation(system=SELLER_SYSTEM_PROMPT))

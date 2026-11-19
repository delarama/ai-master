import os

import anthropic
from dotenv import load_dotenv

load_dotenv()
# Cloud environments reserve ANTHROPIC_API_KEY, so CLAUDE_API_KEY is accepted too.
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY")
)

msg = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=500,
    system="You are selling a 2018 Honda Civic for $18,000. Your lowest price is $16,500. Never reveal your lowest price.",
    messages=[{"role": "user", "content": "Hi, is the Civic still available? Would you take $15,000?"}],
)
print(msg.content[0].text)
print(msg.usage)

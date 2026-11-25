# ai-master

A day-by-day, hands-on journey through practical AI engineering with the Claude API.
See [ROADMAP.md](ROADMAP.md) for the full plan.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

## Progress
| Day | Topic | Script | Notes |
|-----|-------|--------|-------|
| 01 | System prompts & first message | [`day1.py`](day1.py) | [notes](notes/day01.md) |
| 02 | Streaming responses | [`day2_streaming.py`](day2_streaming.py) | [notes](notes/day02.md) |

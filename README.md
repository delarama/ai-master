# ai-master

![CI](https://github.com/delarama/ai-master/actions/workflows/ci.yml/badge.svg)

A day-by-day, hands-on journey through practical AI engineering with the Claude API.
See [ROADMAP.md](ROADMAP.md) for the full plan.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then paste your key into .env
```

## Development
```bash
pip install -r requirements-dev.txt
ruff check .   # lint
pytest -q      # tests (mocked, no API key needed)
```
Shared setup lives in [`common.py`](common.py). CI runs lint and tests on every pull request.

## Progress
| Day | Topic | Script | Notes |
|-----|-------|--------|-------|
| 01 | System prompts & first message | [`day1.py`](day1.py) | [notes](notes/day01.md) |
| 02 | Streaming responses | [`day2_streaming.py`](day2_streaming.py) | [notes](notes/day02.md) |
| 03 | Multi-turn conversations | [`day03_multiturn.py`](day03_multiturn.py) | [notes](notes/day03.md) |
| 04 | Temperature, max_tokens & stop sequences | [`day04_sampling_params.py`](day04_sampling_params.py) | [notes](notes/day04.md) |

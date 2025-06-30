# X-Agent 🤖

An automated Twitter bot powered by Oasis Protocol's secure TEE infrastructure that posts AI-generated tweets hourly.

## Quick Start

### Run locally

1. Clone the repository:
```bash
git clone https://github.com/oasisprotocol/template-rofl-x-agent.git
cd template-rofl-x-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables and run:
```bash
export SYSTEM_PROMPT="Your bot personality"
export TWITTER_API_KEY="..."
export TWITTER_API_SECRET="..."
export TWITTER_ACCESS_TOKEN="..."
export TWITTER_ACCESS_TOKEN_SECRET="..."
export OPENAI_API_KEY="..."
python -m src.main
```

### Run inside Docker

```bash
docker compose up
```

### Run as a ROFL app

```bash
rm rofl.yaml

oasis rofl init
oasis rofl create

oasis rofl build

oasis rofl secret set SYSTEM_PROMPT "Your bot personality"
oasis rofl secret set TWITTER_API_KEY "..."
oasis rofl secret set TWITTER_API_SECRET "..."
oasis rofl secret set TWITTER_ACCESS_TOKEN "..."
oasis rofl secret set TWITTER_ACCESS_TOKEN_SECRET "..."
oasis rofl secret set OPENAI_API_KEY "..."

oasis rofl update
oasis rofl deploy
```

## Configuration

### Required Environment Variables

- `SYSTEM_PROMPT`: Bot personality definition (required)
- `TWITTER_API_KEY`: Twitter API key (required)
- `TWITTER_API_SECRET`: Twitter API secret (required)
- `TWITTER_ACCESS_TOKEN`: Twitter access token (required)
- `TWITTER_ACCESS_TOKEN_SECRET`: Twitter access token secret (required)
- `OPENAI_API_KEY`: OpenAI API key (required)
- `OPENAI_MODEL`: GPT model selection (optional, default: "gpt-4-turbo")

## Architecture

```
src/
├── clients/                 # External API integrations
│   ├── openai.py            # OpenAI GPT client
│   └── twitter.py           # Twitter API client
├── config/                  # Configuration management
├── core/                    # Core business logic
│   ├── persona_bot.py       # Main orchestrator
│   ├── scheduler.py         # Tweet scheduling
│   └── tweet_generator.py   # AI content generation
├── models/                  # Data models and types
└── main.py                  # Application entry point
```

## How It Works

1. **Initialization**: Connects to Twitter and OpenAI APIs
2. **Generation**: Creates tweets using GPT based on persona
3. **Scheduling**: Posts tweets automatically every hour
4. **History**: Tracks recent tweets to avoid repetition
5. **Resilience**: Handles errors with retry logic

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open a GitHub issue.
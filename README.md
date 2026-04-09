# Slack AI Agent v2

A clean, minimal Slack bot with AI capabilities for document search and CSV analysis.

## Features

- 🤖 **AI-powered conversations** using OpenAI GPT-4o-mini
- 📚 **Document search** with RAG (Retrieval Augmented Generation)
- 📊 **CSV data analysis** with automatic pandas code generation
- 💬 **Thread-aware conversations** with context memory
- 🔍 **Vector search** using ChromaDB and OpenAI embeddings

## Quick Start

1. **Clone and setup**
   ```bash
   cd slack-csv-analyzer
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Add your content**
   - Place knowledge documents in `docs/knowledge/` (`.txt` files)
   - Place CSV files in `docs/csvs/` (`.csv` files)

4. **Run the bot**
   ```bash
   python main.py
   ```

## Environment Variables

Required variables in your `.env` file:

```bash
SLACK_APP_TOKEN=xapp-1-YOUR-APP-TOKEN-HERE
SLACK_BOT_TOKEN=xoxb-YOUR-BOT-TOKEN-HERE
OPENAI_API_KEY=sk-YOUR-OPENAI-API-KEY-HERE
LOG_LEVEL=INFO  # Optional: DEBUG, INFO, WARNING, ERROR
```

## Slack App Setup

1. Go to [api.slack.com](https://api.slack.com/apps) and create a new app
2. Enable **Socket Mode** and generate an App Token
3. Add **Bot Token Scopes**: `app_mentions:read`, `chat:write`, `commands`
4. Install app to your workspace and copy the Bot Token
5. Enable **Event Subscriptions** and subscribe to `app_mention` events

## Usage

### In Slack

- **Ask questions**: `@bot What is our company policy on remote work?`
- **Analyze data**: `@bot What are the top 5 products by revenue this quarter?`
- **Get help**: `/help`

### File Structure

```
slack-csv-analyzer/
├── main.py              # Main application
├── tools/               # Tool modules
│   ├── agent.py         # AI agent with tools
│   ├── vectorstore.py   # Document vector search
│   ├── document_search.py  # Search tool
│   ├── csv_analyzer.py  # CSV analysis tool
│   └── storage.py       # Chat storage
├── docs/               # Content directory
│   ├── knowledge/      # Text documents
│   └── csvs/          # CSV data files
├── .env.example       # Environment template
└── pyproject.toml     # Dependencies
```

## Architecture

- **Minimal Dependencies**: Only essential packages
- **Simple Agent**: LangChain agents with tool calling
- **Clean Storage**: SQLite for chat history
- **Safe Execution**: Sandboxed pandas code execution
- **Modular Design**: Easy to extend and maintain

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Format code:
```bash
black .
ruff check .
```

## License

MIT License
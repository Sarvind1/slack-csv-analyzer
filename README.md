# Slack Supply Chain Agent

A Slack bot that leverages AI to analyze supply chain data, answer questions about CSV datasets, and search knowledge bases. Built with LangChain, Chroma, and OpenAI, it provides real-time access to OTIF (On-Time In-Full), booking, and FBA data through natural language queries.

## Features

- **Natural Language Queries**: Ask questions about supply chain data in plain English
- **CSV Analysis**: Intelligent pandas code generation for analyzing CSV datasets
- **Document Search**: Vector-based search across knowledge bases and CSV column references
- **Chat History**: Persistent conversation storage with thread support
- **Supply Chain Focus**: Pre-loaded with domain knowledge for OTIF, bookings, and FBA data
- **Event Deduplication**: Prevents duplicate message processing

## Tech Stack

- **Framework**: Python 3 with Slack Bolt
- **AI/ML**: LangChain + LangGraph, OpenAI GPT-4o-mini
- **Vector Store**: Chroma with OpenAI embeddings
- **Data Processing**: pandas
- **Storage**: SQLite for chat history
- **Dependency Manager**: uv

## Setup

### Prerequisites

- Python 3.9+
- Slack workspace with app creation permissions
- OpenAI API key
- Slack Bot and App tokens

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd slack-supply-chain-agent
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   # or: pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Fill in your `.env` file with:
   - `SLACK_BOT_TOKEN`: xoxb-... token from your Slack app
   - `SLACK_APP_TOKEN`: xapp-... token for socket mode
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `LOG_LEVEL`: Optional, defaults to INFO

### Knowledge Base Setup

Place your CSV files and documentation in:
- `docs/csvs/` — Your data CSV files
- `docs/knowledge/` — Knowledge base documents
- `docs/knowledge/column_references/` — CSV column documentation
- `docs/knowledge/csv_descriptions/` — Detailed CSV explanations

The vector store will automatically index these documents on first run.

## Usage

### Running the Bot

```bash
python main.py
```

The bot will connect to Slack and listen for mentions (@bot-name).

### Local Testing

Test the agent without Slack connection:

```bash
python local_test.py
```

This interactive interface lets you test queries and agent responses.

## Example Queries

- "What's the OTIF rate for Q1?"
- "Show me bookings from the last 7 days"
- "Analyze the FBA emailer data and find trends"
- "Which columns are available in the OnTime_Data table?"

## Architecture

- **`main.py`** — Slack bot entry point with event handlers
- **`local_test.py`** — Standalone testing interface
- **`tools/agent.py`** — LangGraph AI agent with tool integration
- **`tools/csv_analyzer.py`** — CSV analysis with AI-generated pandas code
- **`tools/document_search.py`** — Vector store document retrieval
- **`tools/vector_store.py`** — Chroma vector database management
- **`tools/registry.py`** — Document registry and change tracking
- **`tools/storage.py`** — Chat history storage

## Logging

Logs are written to:
- `slack_ai_agent.log` — Production bot logs
- `local_test.log` — Test interface logs

Check `LOG_LEVEL` environment variable to adjust verbosity.

## License

Proprietary
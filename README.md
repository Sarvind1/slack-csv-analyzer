# Slack AI Agent

An AI-powered Slack bot that provides intelligent document search and CSV data analysis using LangChain, OpenAI, and vector embeddings. Built for enterprise knowledge bases and operational data queries.

## Features

- **AI-Powered Chat**: Real-time conversation in Slack using OpenAI's GPT-4o-mini model
- **Document Search**: Semantic search across knowledge bases using vector embeddings (RAG)
- **CSV Data Analysis**: Automatic pandas code generation and execution for data queries
- **Conversation Context**: Thread-aware chat history with context-aware query enhancement
- **Safe Execution**: Sandboxed code execution for generated pandas analysis
- **Deduplication**: Automatic handling of Slack event retries to prevent duplicate responses
- **Production Ready**: Comprehensive logging, error handling, and SQLite chat storage

## Tech Stack

- **Python 3.11+**
- **Slack Bolt**: Native Slack bot framework with Socket Mode
- **LangChain/LangGraph**: AI agent orchestration and tool integration
- **OpenAI**: GPT-4o-mini for chat, text-embedding-3-large for vectors
- **ChromaDB**: Vector database for semantic search
- **Pandas**: CSV data analysis and manipulation
- **SQLite**: Conversation history and chat logs

## Setup

### Prerequisites
- Python 3.11 or higher
- Slack workspace with bot token
- OpenAI API key

### Installation

1. Clone and create virtual environment:
```bash
git clone <repo-url>
cd slack-ai-agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -e .
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials:
# - SLACK_APP_TOKEN (xapp-1-...)
# - SLACK_BOT_TOKEN (xoxb-...)
# - OPENAI_API_KEY (sk-...)
```

4. Organize your knowledge base:
```bash
mkdir -p docs/knowledge/csv_descriptions docs/knowledge/column_references docs/csvs
# Place .md files in docs/knowledge/
# Place .csv files in docs/csvs/
```

5. Run the bot:
```bash
python main.py
```

For local testing without Slack:
```bash
python local_test.py
```

## Usage

### In Slack

Mention the bot to ask questions:

```
@OTIS what were our top OTIF metrics last month?
@OTIS analyze booking data for batch BATCH0010772
@OTIS show me supplier performance trends
```

The bot automatically:
- Searches your knowledge base for relevant context
- Analyzes CSV data with AI-generated pandas code
- Formats responses using Slack markdown
- Maintains conversation context within threads

### Local Testing

Run `python local_test.py` for interactive testing:

```
👤 You: What's in the OnTime_Data?
🤖 Assistant: The OnTime_Data CSV contains...
```

## Project Structure

```
slack-ai-agent/
├── main.py                    # Slack bot entry point
├── local_test.py              # Local testing interface
├── pyproject.toml             # Dependencies
├── .env.example               # Environment template
│
├── tools/
│   ├── agent.py               # LangGraph AI agent with tools
│   ├── vector_store.py        # ChromaDB vector operations
│   ├── vectorstore.py         # High-level vector store interface
│   ├── registry.py            # File change tracking
│   ├── document_search.py     # Knowledge base search tool
│   ├── csv_analyzer.py        # Data analysis tool
│   └── storage.py             # Chat history (SQLite)
│
├── docs/
│   ├── knowledge/
│   │   ├── csv_descriptions/  # Dataset documentation
│   │   └── column_references/ # Column mappings
│   └── csvs/                  # Data files for analysis
│
└── chat_logs/                 # (auto-created) Conversation history
```

## Architecture

The agent uses a two-layer architecture:

1. **Registry System**: Tracks file changes via hashing to efficiently update the vector store only when documents change
2. **Vector Operations**: ChromaDB with OpenAI embeddings for semantic search across documents

The bot automatically:
- Enhances user queries (resolves pronouns, maps business terms)
- Routes queries to document search or CSV analyzer
- Generates and executes safe pandas code
- Maintains thread-aware conversation context

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SLACK_APP_TOKEN` | Slack app-level token | `xapp-1-...` |
| `SLACK_BOT_TOKEN` | Slack bot user token | `xoxb-...` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `LOG_LEVEL` | Logging level (optional) | `INFO`, `DEBUG` |

### File Naming Conventions

For proper CSV analysis, maintain consistent naming:
- CSV file: `dataset_name.csv` (e.g., `otif_pull.csv`)
- Description: `dataset_name.md` (e.g., `otif_pull.md`)
- Columns: `dataset_name_columns.md` (e.g., `otif_pull_columns.md`)

## Development

Format and lint code:
```bash
black .
ruff check .
```

Run tests (if available):
```bash
pytest
```

## Logging

The bot logs to both console and file (`slack_ai_agent.log`) with:
- Query enhancement details
- Tool selection and execution
- Duplicate event detection
- CSV analysis code and results
- All API interactions

## Security

- No credentials stored in code—use `.env` for sensitive data
- CSV code executed in sandboxed environment with restricted builtins
- Event deduplication prevents unintended duplicate responses
- All API calls logged (without exposing credentials)

## License

MIT

## Support

For issues or questions, check the logs in `slack_ai_agent.log` or review the CLAUDE.md file for detailed architecture notes.
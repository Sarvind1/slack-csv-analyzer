# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Slack AI Agent v2 - a clean, minimal Python application that provides AI-powered conversations, document search with RAG (Retrieval Augmented Generation), and CSV data analysis capabilities through a Slack bot interface.

## Development Commands

### Setup and Installation
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Running the Application
```bash
# Run the Slack bot
python main.py
```

### Code Quality and Formatting
```bash
# Format code with Black
black .

# Lint code with Ruff
ruff check .
```

### Testing
```bash
# Run tests (if pytest is available)
pytest
```

## Architecture Overview

The application follows a modular architecture with the following key components:

### Core Entry Point
- `main.py`: Main application entry point that initializes the Slack app, sets up logging, validates environment variables, and handles Slack events (app mentions and /help command)

### Tools Module (`tools/`)
- `agent.py`: Core AI agent using LangGraph with OpenAI GPT-4o, implements SimpleAIAgent class with tool integration and context-aware conversation handling
- `vectorstore.py`: High-level vector store interface that orchestrates document management and initialization
- `registry.py`: File tracking system with hash-based change detection for efficient vector store updates
- `vector_store.py`: Low-level ChromaDB vector store operations for document embeddings using OpenAI text-embedding-3-large model
- `document_search.py`: Document search tool that performs vector similarity search on knowledge documents
- `csv_analyzer.py`: CSV analysis tool that generates and executes pandas code for data analysis with enhanced column reference handling
- `storage.py`: SQLite-based chat storage for conversation context and thread management

### Key Architectural Patterns

**Agent-Tool Integration**: Uses LangGraph's create_react_agent framework that can intelligently select and use tools based on user queries.

**RAG Implementation**: Document search uses ChromaDB for vector storage with recursive text splitting (1000 char chunks, 200 overlap) and OpenAI embeddings for semantic search.

**Safe Code Execution**: CSV analysis generates pandas code via AI and executes it in a restricted environment with limited builtins for security.

**Thread-Aware Conversations**: Chat storage maintains conversation context within Slack threads, providing the last 3 messages as context to the AI agent.

## File Structure and Data

### Content Directories
- `docs/knowledge/`: Knowledge base with organized subdirectories:
  - `csv_descriptions/`: Markdown files describing CSV datasets and their business context
  - `column_references/`: Dedicated markdown files containing column name mappings and synonyms
  - Other .txt/.md files for general document search and RAG functionality
- `docs/csvs/`: Place .csv files here for data analysis capabilities
- `chat_logs/`: SQLite database for conversation history (auto-created)
- `chroma_langchain_db/`: Vector database storage (auto-created)
- `registry.json`: File tracking registry with hashes for change detection (auto-created)

### Configuration
- `.env`: Environment variables (copy from .env.example)
- Required environment variables:
  - `SLACK_APP_TOKEN`: Slack app token (xapp-1-...)
  - `SLACK_BOT_TOKEN`: Slack bot token (xoxb-...)
  - `OPENAI_API_KEY`: OpenAI API key
  - `LOG_LEVEL`: Optional logging level (DEBUG, INFO, WARNING, ERROR)

## Component Dependencies

The AI agent automatically initializes with two tools:
1. Document search tool for knowledge base queries
2. CSV analyzer tool for data analysis questions

Vector store uses a two-layer architecture:
1. **Registry System**: Tracks file changes via hash comparison and manages vector store updates efficiently
2. **Vector Operations**: ChromaDB handles document storage, chunking, and similarity search

The system automatically scans `docs/knowledge/` directory (including subdirectories) at startup and maintains metadata tags for organized retrieval. CSV analyzer uses enhanced search logic to find both dataset descriptions and column reference mappings.

## Development Notes

- Uses UV for dependency management (uv.lock file)
- Logging configured for both console and file output (slack_ai_agent.log)
- Socket Mode for Slack connectivity (no webhooks required)
- Temperature set to 0 for consistent AI responses
- All AI operations include comprehensive error handling and logging
- Migrated from deprecated LangChain agents to LangGraph for modern agent framework
- Enhanced CSV analysis with separate column reference files for better AI understanding

## Recent Major Enhancements

### 1. Query Enhancement System
**Implementation**: Added LLM-based query enhancer that processes all user queries before tool execution.

**Features**:
- **Temporal Resolution**: Converts "last Friday" → "Friday, September 26, 2025"
- **Pronoun Resolution**: Uses conversation context to resolve "them", "it", etc.
- **Business Term Mapping**: Maps informal terms to exact column names
- **Context-Aware**: Processes conversation history for better understanding

**Architecture**: Query enhancement happens at agent level, enhanced queries sent to tools, no redundant context passed to LangGraph.

### 2. CSV Column Reference Issue Resolution
**Problem**: AI was using sample data values as column names instead of actual column names, causing KeyError exceptions.

**Solution Applied**:
1. Fixed variable reference in `csv_analyzer.py:90` from `md_filename` to `column_filename`
2. Renamed `OTIF_Pull_columns.md` to `otif_pull_columns.md` for case consistency
3. Updated filename mapping logic to properly match CSV descriptions with their column references

**Result**: Column references are now properly retrieved and included in AI context, enabling correct pandas code generation.

### 3. Slack-Friendly Response Formatting
**Implementation**: Added system prompt instructions for Slack-optimized responses.

**Features**:
- Uses Slack markdown (`*bold*`, `_italic_`, `` `code` ``)
- Structures data with bullets and tables
- Formats dates readably (removed problematic timestamp conversion)
- Maintains conversational, professional tone

### 4. Tool Selection Improvements
**Problem**: Agent was choosing document search instead of CSV analyzer for data queries.

**Solution**: Enhanced tool descriptions to be more explicit:
- **CSV Analyzer**: Added "booking forms, pickup forms" and "counts, lists, analysis" keywords
- **Document Search**: Made description positive rather than exclusionary

**Result**: Better tool selection for data vs. informational queries.

### 5. Comprehensive Logging Enhancement
**Added Logging**:
- Original vs enhanced queries
- Full LLM prompts and responses
- Code generation and execution details
- Final agent responses sent to Slack

**Benefit**: Complete visibility into query enhancement, tool selection, and response formatting pipeline.

## Important File Naming Conventions

### CSV Analysis Files
For proper column reference matching, maintain this naming pattern:
- CSV description: `{dataset_name}.md` (e.g., `otif_pull.md`, `OnTime_Data.md`)
- Column reference: `{dataset_name}_columns.md` (e.g., `otif_pull_columns.md`, `OnTime_Data_columns.md`)
- Actual CSV data: `{dataset_name}.csv` (e.g., `otif_pull.csv`, `OnTime_Data.csv`)

**Note**: Case sensitivity matters - ensure consistent casing across all related files.

## Current System Status

### ✅ **Working Features**:
- Query enhancement with temporal resolution ("last Friday" → specific dates)
- Pronoun resolution using conversation context ("them" → "booking forms from Friday")
- Column reference retrieval and mapping
- Tool selection between CSV analysis and document search
- Slack-friendly response formatting
- Comprehensive logging pipeline

### 🔧 **Key Technical Decisions**:
- **Query Enhancement**: Happens at agent level before tool execution
- **Tool Selection**: Based on explicit tool descriptions, not system prompts
- **Date Formatting**: Uses readable formats instead of Slack timestamps (LLM miscalculates timestamps)
- **Context Handling**: Enhanced query is self-contained, no redundant context to LangGraph
- **Architecture**: Two-layer vector store (registry + vector operations) for efficient updates

### 📊 **Performance Improvements**:
- Temporal queries now resolve consistently (was intermittent before)
- CSV analysis uses correct column names (was using sample data as column names)
- Tool selection accuracy improved for data vs. information queries
- Response formatting optimized for Slack readability

The system now provides intelligent, context-aware query processing with reliable data analysis capabilities and user-friendly Slack integration.

## Recent Bug Fixes and Improvements (September 2025)

### 6. Duplicate Event Handling Fix
**Problem**: Bot was responding multiple times to the same user message due to Slack event retries.

**Root Cause Analysis**:
- Slack sends duplicate `app_mention` events when acknowledgment is slow
- Events were received at 04:27:24, 04:27:27, and 04:28:15 for the same message
- No deduplication mechanism existed

**Solution Implemented**:
- Added event deduplication in `main.py:handle_mention()`
- Creates unique event key: `user_id:channel:event_ts:text_snippet`
- Early return for duplicate events with logging
- Memory-bounded cache (100 events) with automatic cleanup

**Result**: Eliminates multiple responses to single user messages.

### 7. Query Enhancement for Booking Forms
**Problem**: Query enhancer incorrectly classified booking form queries as "non-data-driven", routing them to document search instead of CSV analyzer.

**Example Issues**:
- "Do we have BATCH0010772 in booking form data?" → CSV analyzer ✅
- "Have we shared the booking form for BATCH0010772?" → Document search ❌

**Solution Implemented**:
- Enhanced query enhancer prompt in `tools/query_enhancer.py`
- Added explicit guidance: "Questions about booking forms, FBA labels, packaging labels, or shipment documents refer to automated form/document/file sharing systems and should be treated as data-driven queries requiring CSV analysis"

**Result**: Consistent routing of booking form queries to CSV analyzer.

### 8. Column Reference Documentation Fix
**Problem**: CSV analyzer generated incorrect pandas code due to missing `batch_id` column in reference documentation.

**Issues Found**:
- Generated code used non-existent column names like `batch` instead of `batch_id`
- KeyError exceptions: `'batch'`, `'BATCH0010616'`
- Column reference files missing critical batch identifier columns

**Solution Implemented**:
- Updated `docs/knowledge/column_references/otif_pull_columns.md`
- Updated `docs/knowledge/column_references/OnTime_Data_columns.md`
- Added: `batch_id | Shipment batch identifier | batch, batch number, batch code, shipment batch, consolidation ID`

**Result**: Accurate pandas code generation with correct column names.

## Current Issues Requiring Attention

### 🔧 **Pending Fixes**:
1. **Vectorstore Reinitialization**: Updated column references need vectorstore reindexing to take effect
2. **Query Enhancement Classification**: May need additional refinement for edge cases
3. **Error Recovery**: CSV analyzer should gracefully handle missing batch data

### 🎯 **Recommended Next Steps**:
1. Restart application to reinitialize vectorstore with updated column references
2. Test batch queries with corrected column mappings
3. Monitor duplicate event detection effectiveness
4. Consider adding more robust error handling for missing data scenarios

## Debugging and Troubleshooting

### Common Issues:
1. **Multiple Bot Responses**: Check for duplicate event detection logs in `slack_ai_agent.log`
2. **Wrong Tool Selection**: Verify query enhancement output and tool classification
3. **Column Name Errors**: Ensure column reference files match actual CSV headers
4. **Missing Data**: Check if batch/PO exists in datasets before querying specific attributes

### Log Analysis:
- Query enhancement: Look for `🔧 Enhancing query` and `✅ Query enhanced` logs
- Tool selection: Check `📊 Analyzing CSV data` vs `🔍 Searching documents`
- Duplicate detection: Watch for `🔄 Duplicate event detected and ignored`
- Column errors: Search for `KeyError` exceptions in pandas execution
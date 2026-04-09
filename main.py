#!/usr/bin/env python3
"""
Slack AI Agent v2 - Clean and minimal implementation
"""

import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from tools.agent import create_ai_agent
from tools.storage import ChatStorage
from tools.vectorstore import initialize_vectorstore

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("slack_ai_agent.log"),
    ],
)

logger = logging.getLogger(__name__)

# Validate environment variables
bot_token = os.getenv("SLACK_BOT_TOKEN")
app_token = os.getenv("SLACK_APP_TOKEN")
openai_key = os.getenv("OPENAI_API_KEY")

if not all([bot_token, app_token, openai_key]):
    raise ValueError(
        "Missing required environment variables. Check SLACK_BOT_TOKEN, "
        "SLACK_APP_TOKEN, and OPENAI_API_KEY in your .env file."
    )

# Initialize Slack app
app = App(token=bot_token)

# Initialize components
logger.info("Initializing AI agent components...")
chat_storage = ChatStorage()
initialize_vectorstore()
agent = create_ai_agent()

# Event deduplication cache (stores recent event timestamps)
recent_events = set()

logger.info("✅ Slack AI Agent v2 initialized successfully")


@app.event("app_mention")
def handle_mention(body, say, logger):
    """Handle app mentions with AI agent response."""
    try:
        event = body["event"]
        user_id = event["user"]
        channel = event["channel"]
        text = event["text"]
        thread_ts = event.get("thread_ts", event["ts"])
        event_ts = event["ts"]

        # Event deduplication: Check if we've seen this exact event recently
        event_key = f"{user_id}:{channel}:{event_ts}:{text[:50]}"
        if event_key in recent_events:
            logger.info(f"🔄 Duplicate event detected and ignored: {event_ts}")
            return

        # Add to recent events and clean old ones (keep last 100 events)
        recent_events.add(event_key)
        if len(recent_events) > 100:
            # Remove oldest 20 events to prevent unbounded growth
            for _ in range(20):
                recent_events.pop()

        logger.info(f"Received mention from {user_id} in {channel}: {text[:100]}...")

        # Store user message
        chat_storage.store_message(
            channel=channel,
            thread_ts=thread_ts,
            user_id=user_id,
            message=text,
            role="user"
        )

        # Get thread context for better responses
        context = chat_storage.get_thread_context(channel, thread_ts, limit=5)  #should we also be fetching the initial message here?

        # Get AI response
        response = agent.invoke(text, context=context) #custom function

        # Store and send response
        chat_storage.store_message(
            channel=channel,
            thread_ts=thread_ts,
            user_id="assistant",
            message=response,
            role="assistant"
        )

        say(text=response, thread_ts=thread_ts)

    except Exception as e:
        logger.error(f"Error handling mention: {e}")
        say(text="Sorry, I encountered an error processing your request.", thread_ts=thread_ts)


@app.command("/help")
def handle_help_command(ack, respond):
    """Show help information."""
    ack()
    help_text = """
🤖 **Slack AI Agent v2**

I can help you with:
• General questions and conversations
• Document search and analysis
• CSV data analysis and insights

Just mention me (@agent) in any message and I'll respond!

Example:
`@agent What are our top performing products this quarter?`
    """
    respond(help_text)


if __name__ == "__main__":
    logger.info("🚀 Starting Slack AI Agent v2...")
    handler = SocketModeHandler(app, app_token)
    handler.start()
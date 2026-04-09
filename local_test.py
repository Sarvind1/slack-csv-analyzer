#!/usr/bin/env python3
"""
Local testing agent - runs AI agent without Slack connection
"""

import os
import logging
from dotenv import load_dotenv
from datetime import datetime

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
        logging.FileHandler("local_test.log"),
    ],
)

logger = logging.getLogger(__name__)

# Validate OpenAI key
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError(
        "Missing OPENAI_API_KEY environment variable. Check your .env file."
    )

# Initialize components
logger.info("Initializing AI agent components...")
chat_storage = ChatStorage(storage_dir="chat_logs_local_test")
initialize_vectorstore()
agent = create_ai_agent()

logger.info("✅ Local test agent initialized successfully")


def simulate_conversation():
    """Simulate a conversation with the AI agent."""
    print("\n" + "="*60)
    print("🤖 Local AI Agent Test Interface")
    print("="*60)
    print("\nType your messages below. Commands:")
    print("  - 'quit' or 'exit': Exit the program")
    print("  - 'clear': Clear conversation context")
    print("  - 'context': Show current conversation context")
    print("="*60 + "\n")

    # Simulate a channel and thread
    channel = "local_test"
    thread_ts = datetime.now().isoformat()
    user_id = "test_user"

    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ["quit", "exit"]:
                print("\n👋 Goodbye!")
                break

            if user_input.lower() == "clear":
                # Start a new thread
                thread_ts = datetime.now().isoformat()
                print("\n🔄 Conversation context cleared!")
                continue

            if user_input.lower() == "context":
                context = chat_storage.get_thread_context(channel, thread_ts, limit=10)
                print("\n📜 Current conversation context:")
                if not context:
                    print("  (empty)")
                else:
                    for msg in context:
                        role = "👤 User" if msg["role"] == "user" else "🤖 Assistant"
                        timestamp = msg["timestamp"]
                        content = msg["message"][:100] + "..." if len(msg["message"]) > 100 else msg["message"]
                        print(f"  {role} [{timestamp}]: {content}")
                continue

            # Store user message
            chat_storage.store_message(
                channel=channel,
                thread_ts=thread_ts,
                user_id=user_id,
                message=user_input,
                role="user"
            )

            # Get thread context
            context = chat_storage.get_thread_context(channel, thread_ts, limit=5)

            # Get AI response
            print("\n🤖 Assistant: ", end="", flush=True)
            response = agent.invoke(user_input, context=context)
            print(response)

            # Store assistant response
            chat_storage.store_message(
                channel=channel,
                thread_ts=thread_ts,
                user_id="assistant",
                message=response,
                role="assistant"
            )

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error during conversation: {e}")
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    logger.info("🚀 Starting local test agent...")
    simulate_conversation()

"""
AI Agent with tool integration using LangGraph
"""

import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate

from .document_search import create_document_search_tool
from .csv_analyzer import create_csv_analyzer_tool

logger = logging.getLogger(__name__)


class SimpleAIAgent:
    """Simple AI agent with document search and CSV analysis capabilities."""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.tools = self._create_tools()
        # Create system prompt for Slack-friendly responses
        slack_prompt = ChatPromptTemplate.from_messages([
            ("system", """
You are OTIS, a friendly AI assistant for supply chain and data queries. 
Always format messages using Slack `mrkdwn` for clarity.

Guidelines:
- Highlight key info with `_italics_`, or `` `inline code` `` for numbers, IDs, and metrics.
- For tables, use bulleted or numbered lists.
- Keep sentences concise, friendly, and actionable.
"""),
("placeholder", "{messages}"),
        ])

        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=slack_prompt,
        )

    def _create_tools(self) -> list:
        """Create and return available tools."""
        return [
            create_csv_analyzer_tool(),
            create_document_search_tool(),
        ]

    def invoke(self, query: str, context: List[Dict[str, Any]] = None) -> str:
        """Process query with optional conversation context."""
        try:
            # Step 1: Get context for query enhancement
            context_str = None
            if context:
                context_str = self._format_context(context)
                logger.debug(f"Context for query: {context_str}")

            # Step 2: Enhance the user query with context for pronoun resolution
            from .query_enhancer import enhance_user_query
            enhanced_query = enhance_user_query(query, context_str)
            logger.info(f"📊 Original query: {query}")
            logger.info(f"🔧 Enhanced query: {enhanced_query}")

            # Step 3: Use only enhanced query (context already resolved)
            full_query = enhanced_query

            logger.info(f"Processing enhanced query: {enhanced_query[:100]}...")
            logger.info(f"📤 Full Agent Query sent to LangGraph:\n{full_query}")

            # LangGraph uses invoke instead of run and expects messages format
            response = self.agent.invoke({"messages": [("user", full_query)]})

            # Extract the final response from LangGraph output
            final_message = response["messages"][-1]
            if hasattr(final_message, 'content'):
                result = final_message.content
            else:
                result = str(final_message)

            logger.info("✅ Agent response generated successfully")
            logger.info(f"📤 Final Agent Response sent to Slack:\n{result}")

            return result

        except Exception as e:
            logger.error(f"Agent error: {e}")
            return f"I encountered an error processing your request: {str(e)}"

    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """Format conversation context for the agent."""
        formatted = []
        for msg in context[-3:]:  # Last 3 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["message"][:200] + "..." if len(msg["message"]) > 200 else msg["message"]
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)


def create_ai_agent() -> SimpleAIAgent:
    """Factory function to create AI agent."""
    return SimpleAIAgent()
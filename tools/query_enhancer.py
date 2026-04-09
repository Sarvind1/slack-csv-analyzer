"""
Simple LLM-based Query Enhancer
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Optional
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class QueryEnhancer:
    """Simple LLM-based query enhancer using prompt engineering."""

    def __init__(self):
        """Initialize the query enhancer."""
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    def enhance_query(self, user_query: str, conversation_context: str = None) -> str:
        """
        Enhance user query using LLM with detailed business context.

        Args:
            user_query: Original user query
            conversation_context: Previous conversation for resolving pronouns/references

        Returns:
            Enhanced query string
        """
        try:
            logger.info(f"🔧 Enhancing query: {user_query}")

            enhancement_prompt = self._create_enhancement_prompt(user_query, conversation_context)

            logger.info(f"📤 Query enhancement prompt sent to LLM")
            response = self.llm.invoke(enhancement_prompt)

            enhanced_query = response.content.strip()
            logger.info(f"✅ Query enhanced: {enhanced_query}")

            return enhanced_query

        except Exception as e:
            logger.error(f"❌ Query enhancement failed: {e}")
            return user_query  # Fallback to original query

    def _create_enhancement_prompt(self, user_query: str, conversation_context: str = None) -> str:
        """Create the enhancement prompt with business context."""

        # Build context section
        context_section = ""
        if conversation_context:
            context_section = f"""
CONVERSATION CONTEXT: A list of previous messages in the slack conversation
{conversation_context}

"""

        prompt = f"""Rewrite the query to be clear and unambiguous, and mark whether it's data-driven or non-data.

Today's date is {datetime.now().strftime('%Y-%m-%d')}.
{context_section}
Business shorthand:
A 5-digit number like 72226 represents a supplier ID (supplier ID + supplier name).
A code like PO323456 refers to a purchase order (document number).
A person's name such as Joey Wang or Paul Fong refers to a supplier manager (SM), category manager (CM), or final POC
A Razin is an SKU like WIGA-000095 (letters-numbers pattern), and asin is Amazon Standard Identification Number (10 characters, letters and numbers).
Questions about booking forms, FBA labels, packaging labels, or shipment documents refer to automated form/document/file sharing systems and should be treated as data-driven queries requiring CSV analysis.
A "days bucket" refers to a range of days for processing time in format "XX-XX", such as "01-03" for 1 to 3 days, "04-08" for 4 to 8 days. Always use the exact format "04-08" not "4 to 8" or "4-8".
A PO contains batches, and batches contains Razins (SKUs), indirectly POs contain Razins. 
PO value of a line is calculated as quantity * unit price.

Things to add to your response:
If user query has short names like "Joey" which typically refer to full names like "Joey Wang" then mention the need to search in a smarter way as this might be a short name


USER QUERY: "{user_query}"
"""

        return prompt


def enhance_user_query(query: str, conversation_context: str = None) -> str:
    """
    Convenience function to enhance a user query.

    Args:
        query: User query to enhance
        conversation_context: Previous conversation for resolving pronouns/references

    Returns:
        Enhanced query string
    """
    enhancer = QueryEnhancer()
    return enhancer.enhance_query(query, conversation_context)
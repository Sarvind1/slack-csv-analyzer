"""
Document search tool using vector store
"""

import logging
from langchain.tools import Tool
from .vectorstore import get_vectorstore

logger = logging.getLogger(__name__)


def search_documents(query: str) -> str:
    """Search documents using vector similarity."""
    try:
        logger.info(f"🔍 Searching documents for: {query}")

        vectorstore = get_vectorstore()
        docs = vectorstore.similarity_search(query, k=5)

        if not docs:
            return "No relevant documents found for your query."

        # Format results
        results = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content
            results.append(f"**Document {i}** (Source: {source}):\n{content}")

        response = "Here's what I found in the documents:\n\n" + "\n\n".join(results)
        logger.info(f"✅ Found {len(docs)} relevant documents")

        return response

    except Exception as e:
        logger.error(f"❌ Document search error: {e}")
        return f"Error searching documents: {str(e)}"


def create_document_search_tool() -> Tool:
    """Create document search tool."""
    return Tool(
        name="search_documents",
        description="Search knowledge base documents for general information, process explanations, definitions, and conceptual questions. Use when users ask 'what is', 'how do I', 'explain', or need background information rather than specific data analysis.",
        func=search_documents,
    )
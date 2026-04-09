"""
Vector store management - now uses registry system for flexible document loading
"""

import logging
from typing import Optional

from .registry import create_registry
from .vector_store import create_vector_store_manager

logger = logging.getLogger(__name__)


def initialize_vectorstore() -> None:
    """Initialize vector store by scanning knowledge directory."""
    try:
        logger.info("🔍 Initializing vector store using registry...")

        registry = create_registry()

        # Scan knowledge directory
        from pathlib import Path
        knowledge_dir = Path("docs/knowledge")

        if knowledge_dir.exists():
            logger.info("📖 Scanning knowledge directory...")
            results = registry.scan(
                str(knowledge_dir),
                file_patterns=["*.txt", "*.md"]
            )
            logger.info(f"Knowledge scan: {results}")
        else:
            logger.warning("📁 docs/knowledge directory not found")

        logger.info("✅ Vector store initialized successfully")

    except Exception as e:
        logger.error(f"❌ Error initializing vector store: {e}")
        raise


def get_vectorstore():
    """Get existing vector store instance."""
    try:
        vector_manager = create_vector_store_manager()
        return vector_manager.get_vectorstore()
    except Exception as e:
        logger.error(f"❌ Error getting vector store: {e}")
        raise


# Convenience functions for direct registry access
def register_document(file_path: str, metadata: Optional[dict] = None) -> str:
    """Register a single document."""
    registry = create_registry()
    return registry.register(file_path, metadata)


def scan_directory(folder_path: str, file_patterns: list = None, metadata: Optional[dict] = None) -> dict:
    """Scan a directory and register all matching files."""
    registry = create_registry()
    return registry.scan(folder_path, file_patterns, metadata)
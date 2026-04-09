"""
Vector Store Manager - Handles actual vector database operations
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from uuid import uuid4

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document

logger = logging.getLogger(__name__)

VECTORSTORE_DIR = "./chroma_langchain_db"


class VectorStoreManager:
    """Manages vector database operations."""

    def __init__(self, persist_directory: str = VECTORSTORE_DIR):
        """Initialize vector store manager."""
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def _get_vectorstore(self) -> Chroma:
        """Get or create vector store."""
        try:
            return Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
        except Exception as e:
            logger.error(f"❌ Error getting vector store: {e}")
            raise

    def add_document(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Add a document to the vector store.

        Args:
            file_path: Path to the document
            metadata: Optional metadata to attach

        Returns:
            List of vector IDs for the added chunks
        """
        try:
            file_path = Path(file_path)

            # Load document
            loader = TextLoader(str(file_path))
            documents = loader.load()

            # Add metadata
            for doc in documents:
                doc.metadata["source"] = str(file_path)
                doc.metadata["filename"] = file_path.name
                if metadata:
                    doc.metadata.update(metadata)

            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)

            if not chunks:
                logger.warning(f"⚠️  No chunks created for {file_path}")
                return []


            # Get vector store
            vectorstore = self._get_vectorstore()

            # Generate unique IDs for chunks
            chunk_ids = [str(uuid4()) for _ in chunks]

            # Add to vector store
            vectorstore.add_documents(documents=chunks, ids=chunk_ids)

            logger.info(f"✅ Added {len(chunks)} chunks from {file_path.name}")
            return chunk_ids

        except Exception as e:
            logger.error(f"❌ Error adding document {file_path}: {e}")
            return []

    def delete_documents(self, vector_ids: List[str]) -> bool:
        """
        Delete documents from vector store by their IDs.

        Args:
            vector_ids: List of vector IDs to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            if not vector_ids:
                return True

            vectorstore = self._get_vectorstore()
            vectorstore.delete(ids=vector_ids)

            logger.info(f"🗑️  Deleted {len(vector_ids)} chunks")
            return True

        except Exception as e:
            logger.error(f"❌ Error deleting documents: {e}")
            return False

    def search(self, query: str, k: int = 5) -> List[Document]:
        """
        Search for similar documents.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of similar documents
        """
        try:
            vectorstore = self._get_vectorstore()
            results = vectorstore.similarity_search(query, k=k)

            logger.info(f"🔍 Search returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"❌ Error searching: {e}")
            return []

    def get_vectorstore(self) -> Chroma:
        """
        Get the vector store for direct use.

        Returns:
            Chroma vector store instance
        """
        return self._get_vectorstore()


# Factory function for easy import
def create_vector_store_manager(persist_directory: str = VECTORSTORE_DIR) -> VectorStoreManager:
    """Create a VectorStoreManager instance."""
    return VectorStoreManager(persist_directory)
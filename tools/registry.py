"""
Document Registry - Simple file tracking and vector store management
"""

import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class DocumentRegistry:
    """Simple registry that tracks files and manages vector store updates."""

    def __init__(self, registry_path: str = "./vector_registry.json"):
        """Initialize registry."""
        self.registry_path = Path(registry_path)
        self.registry_data = {}
        self._load_registry()

    def _load_registry(self):
        """Load registry from disk or create new."""
        try:
            if self.registry_path.exists():
                with open(self.registry_path, 'r') as f:
                    self.registry_data = json.load(f)
                logger.info(f"📋 Loaded registry with {len(self.registry_data.get('files', {}))} files")
            else:
                self.registry_data = {"files": {}, "last_updated": datetime.now().isoformat()}
                self._save_registry()
                logger.info("📋 Created new registry")
        except Exception as e:
            logger.error(f"❌ Error loading registry: {e}")
            self.registry_data = {"files": {}, "last_updated": datetime.now().isoformat()}

    def _save_registry(self):
        """Save registry to disk."""
        try:
            self.registry_data["last_updated"] = datetime.now().isoformat()
            with open(self.registry_path, 'w') as f:
                json.dump(self.registry_data, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Error saving registry: {e}")

    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate file hash."""
        try:
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"❌ Error hashing {file_path}: {e}")
            return ""

    def register(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Register a single file - adds to vector store if new or changed.

        Args:
            file_path: Path to the file
            metadata: Optional metadata (source_type, tags, etc.)

        Returns:
            Status: "added", "updated", "unchanged", or "error"
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"❌ File not found: {file_path}")
                return "error"

            file_str = str(file_path)
            current_hash = self._get_file_hash(file_path)

            if not current_hash:
                return "error"

            # Check if file exists in registry
            if file_str in self.registry_data["files"]:
                stored_hash = self.registry_data["files"][file_str].get("hash", "")

                if current_hash == stored_hash:
                    logger.info(f"📄 No changes: {file_path.name}")
                    return "unchanged"
                else:
                    # File changed - update vector store
                    logger.info(f"🔄 File changed: {file_path.name}")

                    # Import here to avoid circular imports
                    from .vector_store import VectorStoreManager
                    vector_manager = VectorStoreManager()

                    # Get old vector IDs and delete them
                    old_vector_ids = self.registry_data["files"][file_str].get("vector_ids", [])
                    if old_vector_ids:
                        vector_manager.delete_documents(old_vector_ids)

                    # Add updated document
                    vector_ids = vector_manager.add_document(file_str, metadata)

                    # Update registry
                    self.registry_data["files"][file_str] = {
                        "hash": current_hash,
                        "vector_ids": vector_ids,
                        "last_processed": datetime.now().isoformat(),
                        "metadata": metadata or {}
                    }

                    self._save_registry()
                    logger.info(f"✅ Updated: {file_path.name}")
                    return "updated"
            else:
                # New file - add to vector store
                logger.info(f"➕ New file: {file_path.name}")

                from .vector_store import VectorStoreManager
                vector_manager = VectorStoreManager()

                # Add new document
                vector_ids = vector_manager.add_document(file_str, metadata)

                # Add to registry
                self.registry_data["files"][file_str] = {
                    "hash": current_hash,
                    "vector_ids": vector_ids,
                    "last_processed": datetime.now().isoformat(),
                    "metadata": metadata or {}
                }

                self._save_registry()
                logger.info(f"✅ Added: {file_path.name}")
                return "added"

        except Exception as e:
            logger.error(f"❌ Error registering {file_path}: {e}")
            return "error"

    def _remove_file(self, file_path: str) -> bool:
        """
        Remove a file from registry and vector store.

        Args:
            file_path: Path to file to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            if file_path not in self.registry_data["files"]:
                return True  # Already not in registry

            # Get vector IDs to delete
            vector_ids = self.registry_data["files"][file_path].get("vector_ids", [])

            if vector_ids:
                # Delete from vector store
                from .vector_store import VectorStoreManager
                vector_manager = VectorStoreManager()
                vector_manager.delete_documents(vector_ids)

            # Remove from registry
            del self.registry_data["files"][file_path]
            self._save_registry()

            logger.info(f"🗑️  Removed: {Path(file_path).name}")
            return True

        except Exception as e:
            logger.error(f"❌ Error removing {file_path}: {e}")
            return False

    def scan(self, folder_path: str, file_patterns: list = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, int]:
        """
        Scan a folder and register all files. Syncs folder state with registry.

        Args:
            folder_path: Path to folder to scan
            file_patterns: List of patterns like ["*.txt", "*.md"] (default: all files)
            metadata: Metadata to apply to all files in folder

        Returns:
            Dict with counts: {"added": 2, "updated": 1, "unchanged": 5, "deleted": 1, "error": 0}
        """
        try:
            folder_path = Path(folder_path)
            if not folder_path.exists():
                logger.error(f"❌ Folder not found: {folder_path}")
                return {"error": 1, "added": 0, "updated": 0, "unchanged": 0, "deleted": 0}

            if file_patterns is None:
                file_patterns = ["*"]

            logger.info(f"📁 Scanning folder: {folder_path}")

            # Find all matching files
            files = []
            for pattern in file_patterns:
                files.extend(folder_path.rglob(pattern))

            # Filter to only files (not directories) and exclude hidden files
            files = [f for f in files if f.is_file() and not f.name.startswith('.')]

            logger.info(f"📄 Found {len(files)} files to process")

            # Get current files on disk
            current_files = set(str(f) for f in files)

            # Get files in registry that belong to this folder
            folder_str = str(folder_path)
            registry_files_in_folder = set(
                file_path for file_path in self.registry_data["files"]
                if file_path.startswith(folder_str)
            )

            # Find deleted files (in registry but not on disk)
            deleted_files = registry_files_in_folder - current_files

            # Process each current file
            results = {"added": 0, "updated": 0, "unchanged": 0, "deleted": 0, "error": 0}

            for file_path in files:
                # Create file-specific metadata
                file_metadata = (metadata or {}).copy()
                file_metadata["filename"] = file_path.name
                file_metadata["folder"] = str(folder_path)

                # Add relative path within scanned folder as tag
                relative_path = file_path.relative_to(folder_path)
                file_metadata["knowledge_path"] = str(relative_path.parent) if relative_path.parent != Path('.') else ""

                # Register the file
                status = self.register(str(file_path), file_metadata)
                results[status] += 1

            # Clean up deleted files
            if deleted_files:
                logger.info(f"🗑️  Cleaning up {len(deleted_files)} deleted files")
                for deleted_file in deleted_files:
                    if self._remove_file(deleted_file):
                        results["deleted"] += 1
                    else:
                        results["error"] += 1

            logger.info(f"✅ Scan complete: {results}")
            return results

        except Exception as e:
            logger.error(f"❌ Error scanning {folder_path}: {e}")
            return {"error": 1, "added": 0, "updated": 0, "unchanged": 0, "deleted": 0}

    def list_files(self) -> list:
        """List all registered files."""
        return list(self.registry_data["files"].keys())

    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        files = self.registry_data["files"]
        total_files = len(files)
        total_chunks = sum(len(file_data.get("vector_ids", [])) for file_data in files.values())

        return {
            "total_files": total_files,
            "total_chunks": total_chunks,
            "last_updated": self.registry_data.get("last_updated"),
            "files": list(files.keys())
        }


# Factory function for easy import
def create_registry(registry_path: str = "./vector_registry.json") -> DocumentRegistry:
    """Create a DocumentRegistry instance."""
    return DocumentRegistry(registry_path)
"""
Memory Bank for Long-term Memory Storage
Implements persistent memory for agents across sessions
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import logging
from collections import defaultdict


class MemoryBank:
    """
    Long-term memory storage for agents
    Stores and retrieves information across sessions
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path
        self.memory: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.logger = logging.getLogger("memory_bank")
        
        # Load existing memory if storage path provided
        if storage_path:
            self.load()
    
    def store(self, session_id: str, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None):
        """Store a value in memory bank"""
        if session_id not in self.memory:
            self.memory[session_id] = {}
        
        self.memory[session_id][key] = {
            "value": value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "access_count": 0
        }
        
        self.logger.debug(f"Stored memory: {session_id}/{key}")
        self.save()
    
    def get(self, session_id: str, key: str, default: Any = None) -> Any:
        """Retrieve a value from memory bank"""
        if session_id in self.memory and key in self.memory[session_id]:
            memory_entry = self.memory[session_id][key]
            memory_entry["access_count"] = memory_entry.get("access_count", 0) + 1
            memory_entry["last_accessed"] = datetime.now().isoformat()
            self.save()
            return memory_entry["value"]
        return default
    
    def get_all(self, session_id: str) -> Dict[str, Any]:
        """Get all memory for a session"""
        return {
            key: entry["value"]
            for key, entry in self.memory.get(session_id, {}).items()
        }
    
    def delete(self, session_id: str, key: Optional[str] = None):
        """Delete memory entry or entire session"""
        if key:
            if session_id in self.memory and key in self.memory[session_id]:
                del self.memory[session_id][key]
                self.logger.debug(f"Deleted memory: {session_id}/{key}")
        else:
            if session_id in self.memory:
                del self.memory[session_id]
                self.logger.debug(f"Deleted session: {session_id}")
        self.save()
    
    def search(self, session_id: str, query: str) -> List[Dict[str, Any]]:
        """Search memory entries by query"""
        results = []
        if session_id in self.memory:
            query_lower = query.lower()
            for key, entry in self.memory[session_id].items():
                value_str = str(entry["value"]).lower()
                if query_lower in key.lower() or query_lower in value_str:
                    results.append({
                        "key": key,
                        "value": entry["value"],
                        "metadata": entry.get("metadata", {}),
                        "timestamp": entry.get("timestamp")
                    })
        return results
    
    def save(self):
        """Save memory to disk"""
        if self.storage_path:
            try:
                # Convert to JSON-serializable format
                serializable = {}
                for session_id, data in self.memory.items():
                    serializable[session_id] = {}
                    for key, entry in data.items():
                        serializable[session_id][key] = {
                            "value": entry["value"],
                            "metadata": entry.get("metadata", {}),
                            "timestamp": entry.get("timestamp"),
                            "access_count": entry.get("access_count", 0)
                        }
                
                with open(self.storage_path, 'w') as f:
                    json.dump(serializable, f, indent=2)
            except Exception as e:
                self.logger.error(f"Error saving memory: {e}")
    
    def load(self):
        """Load memory from disk"""
        if self.storage_path:
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.memory = defaultdict(dict, data)
                self.logger.info(f"Loaded memory from {self.storage_path}")
            except FileNotFoundError:
                self.logger.info("Memory file not found, starting fresh")
            except Exception as e:
                self.logger.error(f"Error loading memory: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory bank statistics"""
        total_sessions = len(self.memory)
        total_entries = sum(len(session_data) for session_data in self.memory.values())
        
        return {
            "total_sessions": total_sessions,
            "total_entries": total_entries,
            "storage_path": self.storage_path
        }

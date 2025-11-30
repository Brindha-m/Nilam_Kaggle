"""
Session Management for Agent System
Implements InMemorySessionService for state management
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import uuid
import logging
from agents.memory_bank import MemoryBank
from agents.base_agent import AgentContext


class InMemorySessionService:
    """
    In-memory session service for managing agent sessions
    Handles session creation, state management, and context compaction
    """
    
    def __init__(self, memory_bank: Optional[MemoryBank] = None, session_timeout: int = 3600):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.memory_bank = memory_bank
        self.session_timeout = session_timeout  # seconds
        self.logger = logging.getLogger("session_manager")
    
    def create_session(
        self,
        user_id: Optional[str] = None,
        initial_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "conversation_history": [],
            "state": initial_context or {},
            "metadata": {}
        }
        
        self.logger.info(f"Created session: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            # Check if session expired
            last_accessed = datetime.fromisoformat(session["last_accessed"])
            if datetime.now() - last_accessed > timedelta(seconds=self.session_timeout):
                self.logger.warning(f"Session {session_id} expired")
                return None
            
            session["last_accessed"] = datetime.now().isoformat()
            return session
        return None
    
    def get_context(self, session_id: str) -> Optional[AgentContext]:
        """Get agent context for a session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return AgentContext(
            session_id=session_id,
            user_id=session.get("user_id"),
            conversation_history=session.get("conversation_history", []),
            memory=self.memory_bank.get_all(session_id) if self.memory_bank else {},
            state=session.get("state", {})
        )
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add message to conversation history"""
        session = self.get_session(session_id)
        if session:
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            session["conversation_history"].append(message)
            
            # Context compaction: keep only last N messages
            max_messages = 50
            if len(session["conversation_history"]) > max_messages:
                # Keep first message (system/initial) and last N-1 messages
                first_msg = session["conversation_history"][0]
                session["conversation_history"] = [first_msg] + session["conversation_history"][-max_messages+1:]
                self.logger.debug(f"Compacted context for session {session_id}")
    
    def update_state(self, session_id: str, key: str, value: Any):
        """Update session state"""
        session = self.get_session(session_id)
        if session:
            session["state"][key] = value
    
    def get_state(self, session_id: str, key: Optional[str] = None) -> Any:
        """Get session state"""
        session = self.get_session(session_id)
        if session:
            if key:
                return session["state"].get(key)
            return session["state"]
        return None
    
    def compact_context(self, session_id: str, keep_recent: int = 20):
        """Manually compact context for a session"""
        session = self.get_session(session_id)
        if session:
            history = session["conversation_history"]
            if len(history) > keep_recent:
                # Keep first message and recent messages
                first_msg = history[0] if history else None
                recent = history[-keep_recent:]
                session["conversation_history"] = ([first_msg] + recent) if first_msg else recent
                self.logger.info(f"Compacted context for session {session_id}: {len(history)} -> {len(session['conversation_history'])} messages")
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.logger.info(f"Deleted session: {session_id}")
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        now = datetime.now()
        expired = []
        
        for session_id, session in self.sessions.items():
            last_accessed = datetime.fromisoformat(session["last_accessed"])
            if now - last_accessed > timedelta(seconds=self.session_timeout):
                expired.append(session_id)
        
        for session_id in expired:
            self.delete_session(session_id)
        
        if expired:
            self.logger.info(f"Cleaned up {len(expired)} expired sessions")
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about sessions"""
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len([
                s for s in self.sessions.values()
                if datetime.now() - datetime.fromisoformat(s["last_accessed"]) < timedelta(seconds=self.session_timeout)
            ])
        }

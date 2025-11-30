"""
A2A (Agent-to-Agent) Protocol
Enables communication between agents
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import logging
from agents.base_agent import AgentMessage, AgentContext
from enum import Enum


class MessageType(Enum):
    """A2A message types"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    QUERY = "query"
    RESULT = "result"


class A2AProtocol:
    """
    Agent-to-Agent communication protocol
    Handles message routing and agent discovery
    """
    
    def __init__(self):
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.message_queue: List[Dict[str, Any]] = []
        self.logger = logging.getLogger("a2a_protocol")
    
    def register_agent(
        self,
        agent_id: str,
        capabilities: List[str],
        endpoint: Optional[str] = None
    ):
        """Register an agent in the A2A network"""
        self.agent_registry[agent_id] = {
            "agent_id": agent_id,
            "capabilities": capabilities,
            "endpoint": endpoint,
            "registered_at": datetime.now().isoformat(),
            "status": "active"
        }
        self.logger.info(f"Registered agent: {agent_id} with capabilities: {capabilities}")
    
    def discover_agents(self, capability: Optional[str] = None) -> List[str]:
        """Discover agents by capability"""
        if capability:
            return [
                agent_id for agent_id, info in self.agent_registry.items()
                if capability in info.get("capabilities", []) and info.get("status") == "active"
            ]
        return [
            agent_id for agent_id, info in self.agent_registry.items()
            if info.get("status") == "active"
        ]
    
    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message_type: MessageType,
        content: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send A2A message"""
        if to_agent not in self.agent_registry:
            raise ValueError(f"Agent {to_agent} not registered")
        
        message = {
            "from": from_agent,
            "to": to_agent,
            "type": message_type.value,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "message_id": f"{from_agent}_{to_agent}_{datetime.now().timestamp()}"
        }
        
        self.message_queue.append(message)
        self.logger.info(f"A2A message: {from_agent} -> {to_agent} ({message_type.value})")
        
        return message
    
    def broadcast(
        self,
        from_agent: str,
        message_type: MessageType,
        content: Any,
        filter_capability: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Broadcast message to multiple agents"""
        target_agents = self.discover_agents(filter_capability) if filter_capability else self.discover_agents()
        target_agents = [a for a in target_agents if a != from_agent]
        
        messages = []
        for agent_id in target_agents:
            msg = self.send_message(from_agent, agent_id, message_type, content)
            messages.append(msg)
        
        self.logger.info(f"Broadcast from {from_agent} to {len(messages)} agents")
        return messages
    
    def query_agent(
        self,
        from_agent: str,
        to_agent: str,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Query another agent (request-response pattern)"""
        message = self.send_message(
            from_agent,
            to_agent,
            MessageType.QUERY,
            {"query": query, "context": context or {}}
        )
        
        # In a real implementation, this would wait for response
        # For now, return the sent message
        return message
    
    def get_messages(
        self,
        agent_id: Optional[str] = None,
        message_type: Optional[MessageType] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get messages from queue with optional filtering"""
        filtered = self.message_queue
        
        if agent_id:
            filtered = [
                m for m in filtered
                if m.get("from") == agent_id or m.get("to") == agent_id
            ]
        
        if message_type:
            filtered = [
                m for m in filtered
                if m.get("type") == message_type.value
            ]
        
        return filtered[-limit:]
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a registered agent"""
        return self.agent_registry.get(agent_id)
    
    def get_network_topology(self) -> Dict[str, Any]:
        """Get network topology of registered agents"""
        return {
            "total_agents": len(self.agent_registry),
            "active_agents": len([a for a in self.agent_registry.values() if a.get("status") == "active"]),
            "agents": {
                agent_id: {
                    "capabilities": info.get("capabilities", []),
                    "status": info.get("status")
                }
                for agent_id, info in self.agent_registry.items()
            },
            "total_messages": len(self.message_queue)
        }
    
    def route_to_capability(
        self,
        from_agent: str,
        capability: str,
        content: Any
    ) -> Dict[str, Any]:
        """Route message to an agent with specific capability"""
        capable_agents = self.discover_agents(capability)
        
        if not capable_agents:
            raise ValueError(f"No agent found with capability: {capability}")
        
        # Route to first available agent (could implement load balancing)
        target_agent = capable_agents[0]
        return self.send_message(
            from_agent,
            target_agent,
            MessageType.REQUEST,
            content
        )

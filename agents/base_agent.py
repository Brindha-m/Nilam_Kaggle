"""
Base Agent Class for Multi-Agent System
Implements core agent functionality with LLM integration
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from enum import Enum


class AgentState(Enum):
    """Agent execution states"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class AgentMessage:
    """Message structure for agent communication"""
    sender: str
    receiver: str
    content: str
    message_type: str = "text"
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "message_type": self.message_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id
        }


@dataclass
class AgentContext:
    """Context information for agent execution"""
    session_id: str
    user_id: Optional[str] = None
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all agents in the multi-agent system
    Implements LLM-powered agent with tools and memory
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        llm_model: Any = None,
        tools: List[Any] = None,
        memory_bank: Any = None
    ):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.llm_model = llm_model
        self.tools = tools or []
        self.memory_bank = memory_bank
        self.state = AgentState.IDLE
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
            "tool_usage": {}
        }
        self.traces = []
        
    def log_trace(self, event: str, data: Dict[str, Any]):
        """Log trace event for observability"""
        trace = {
            "agent_id": self.agent_id,
            "event": event,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.traces.append(trace)
        self.logger.debug(f"Trace: {event}", extra=trace)
    
    def update_metrics(self, metric_name: str, value: Any):
        """Update agent metrics"""
        if metric_name in self.metrics:
            if isinstance(self.metrics[metric_name], (int, float)):
                # For numeric metrics, update accordingly
                if metric_name == "average_response_time":
                    total = self.metrics["total_requests"]
                    current_avg = self.metrics[metric_name]
                    self.metrics[metric_name] = (current_avg * total + value) / (total + 1)
                else:
                    self.metrics[metric_name] += value
            elif isinstance(self.metrics[metric_name], dict):
                self.metrics[metric_name][value] = self.metrics[metric_name].get(value, 0) + 1
    
    @abstractmethod
    def process(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """
        Process incoming message and return response
        Must be implemented by subclasses
        """
        pass
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool by name"""
        self.log_trace("tool_execution_start", {
            "tool_name": tool_name,
            "parameters": parameters
        })
        
        for tool in self.tools:
            if hasattr(tool, 'name') and tool.name == tool_name:
                try:
                    result = tool.execute(**parameters)
                    self.update_metrics("tool_usage", tool_name)
                    self.log_trace("tool_execution_success", {
                        "tool_name": tool_name,
                        "result": str(result)[:100]  # Truncate for logging
                    })
                    return result
                except Exception as e:
                    self.log_trace("tool_execution_error", {
                        "tool_name": tool_name,
                        "error": str(e)
                    })
                    raise
        
        raise ValueError(f"Tool '{tool_name}' not found")
    
    def get_memory(self, key: str, context: AgentContext) -> Any:
        """Retrieve memory from memory bank"""
        if self.memory_bank:
            return self.memory_bank.get(context.session_id, key)
        return context.memory.get(key)
    
    def store_memory(self, key: str, value: Any, context: AgentContext):
        """Store memory in memory bank"""
        if self.memory_bank:
            self.memory_bank.store(context.session_id, key, value)
        else:
            context.memory[key] = value
    
    def pause(self):
        """Pause agent execution (for long-running operations)"""
        if self.state == AgentState.RUNNING:
            self.state = AgentState.PAUSED
            self.log_trace("agent_paused", {})
    
    def resume(self):
        """Resume agent execution"""
        if self.state == AgentState.PAUSED:
            self.state = AgentState.RUNNING
            self.log_trace("agent_resumed", {})
    
    def get_state(self) -> Dict[str, Any]:
        """Get current agent state"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "state": self.state.value,
            "metrics": self.metrics,
            "available_tools": [tool.name for tool in self.tools if hasattr(tool, 'name')]
        }
    
    def get_traces(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent traces for observability"""
        return self.traces[-limit:]

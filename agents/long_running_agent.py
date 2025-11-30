"""
Long-Running Agent with Pause/Resume Support
Demonstrates long-running operations with state management
"""
from typing import Dict, Any, Optional
import time
import json
import logging
from datetime import datetime
from agents.base_agent import BaseAgent, AgentMessage, AgentContext, AgentState
from agents.session_manager import InMemorySessionService


class LongRunningAgent(BaseAgent):
    """
    Agent that demonstrates long-running operations
    with pause/resume functionality
    """
    
    def __init__(
        self,
        agent_id: str = "long_running_agent",
        session_service: InMemorySessionService = None
    ):
        super().__init__(
            agent_id=agent_id,
            agent_name="Long-Running Operation Agent"
        )
        self.session_service = session_service
        self.active_operations: Dict[str, Dict[str, Any]] = {}
    
    def start_long_running_task(
        self,
        task_id: str,
        message: AgentMessage,
        context: AgentContext,
        task_type: str = "data_processing"
    ) -> Dict[str, Any]:
        """Start a long-running task"""
        self.log_trace("long_task_start", {
            "task_id": task_id,
            "task_type": task_type
        })
        
        # Store operation state
        operation = {
            "task_id": task_id,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "progress": 0,
            "message": message,
            "context": context,
            "task_type": task_type,
            "checkpoint": None
        }
        
        self.active_operations[task_id] = operation
        
        # Update session state
        if self.session_service:
            self.session_service.update_state(context.session_id, f"task_{task_id}", operation)
        
        return {
            "task_id": task_id,
            "status": "started",
            "message": f"Long-running task {task_id} started"
        }
    
    def pause_task(self, task_id: str) -> Dict[str, Any]:
        """Pause a long-running task"""
        if task_id not in self.active_operations:
            return {"error": f"Task {task_id} not found"}
        
        operation = self.active_operations[task_id]
        
        if operation["status"] != "running":
            return {"error": f"Task {task_id} is not running"}
        
        # Save checkpoint
        operation["checkpoint"] = {
            "progress": operation["progress"],
            "paused_at": datetime.now().isoformat(),
            "state": operation.get("state", {})
        }
        
        operation["status"] = "paused"
        self.state = AgentState.PAUSED
        
        self.log_trace("task_paused", {
            "task_id": task_id,
            "checkpoint": operation["checkpoint"]
        })
        
        return {
            "task_id": task_id,
            "status": "paused",
            "checkpoint": operation["checkpoint"]
        }
    
    def resume_task(self, task_id: str) -> Dict[str, Any]:
        """Resume a paused task"""
        if task_id not in self.active_operations:
            return {"error": f"Task {task_id} not found"}
        
        operation = self.active_operations[task_id]
        
        if operation["status"] != "paused":
            return {"error": f"Task {task_id} is not paused"}
        
        # Restore from checkpoint
        checkpoint = operation.get("checkpoint", {})
        operation["progress"] = checkpoint.get("progress", 0)
        operation["status"] = "running"
        self.state = AgentState.RUNNING
        
        self.log_trace("task_resumed", {
            "task_id": task_id,
            "resumed_from": checkpoint
        })
        
        return {
            "task_id": task_id,
            "status": "resumed",
            "progress": operation["progress"]
        }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a long-running task"""
        if task_id not in self.active_operations:
            return {"error": f"Task {task_id} not found"}
        
        operation = self.active_operations[task_id]
        return {
            "task_id": task_id,
            "status": operation["status"],
            "progress": operation["progress"],
            "started_at": operation["started_at"],
            "checkpoint": operation.get("checkpoint")
        }
    
    def process(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """Process message - can start long-running tasks"""
        self.state = AgentState.RUNNING
        
        # Check if this is a task management command
        content = message.content.lower()
        
        if "start task" in content or "long running" in content:
            task_id = f"task_{int(time.time())}"
            result = self.start_long_running_task(task_id, message, context)
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=f"Started long-running task: {task_id}. Use pause/resume commands to manage it.",
                metadata={"task_id": task_id},
                session_id=context.session_id
            )
        
        elif "pause" in content:
            # Extract task_id from message or context
            task_id = context.state.get("current_task_id")
            if not task_id:
                return AgentMessage(
                    sender=self.agent_id,
                    receiver=message.sender,
                    content="No active task to pause. Please specify task_id.",
                    session_id=context.session_id
                )
            
            result = self.pause_task(task_id)
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=json.dumps(result, indent=2),
                session_id=context.session_id
            )
        
        elif "resume" in content:
            task_id = context.state.get("current_task_id")
            if not task_id:
                return AgentMessage(
                    sender=self.agent_id,
                    receiver=message.sender,
                    content="No paused task to resume. Please specify task_id.",
                    session_id=context.session_id
                )
            
            result = self.resume_task(task_id)
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=json.dumps(result, indent=2),
                session_id=context.session_id
            )
        
        elif "task status" in content:
            task_id = context.state.get("current_task_id")
            if not task_id:
                return AgentMessage(
                    sender=self.agent_id,
                    receiver=message.sender,
                    content="No task_id specified.",
                    session_id=context.session_id
                )
            
            result = self.get_task_status(task_id)
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=json.dumps(result, indent=2),
                session_id=context.session_id
            )
        
        else:
            # Regular processing
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content="I'm a long-running operation agent. Use commands like 'start task', 'pause', 'resume', or 'task status'.",
                session_id=context.session_id
            )





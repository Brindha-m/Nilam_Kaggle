"""
Multi-Agent Orchestrator
Implements parallel, sequential, and loop agent patterns
"""
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import asyncio
import logging
from agents.base_agent import BaseAgent, AgentMessage, AgentContext
from agents.session_manager import InMemorySessionService


class AgentPattern(Enum):
    """Agent execution patterns"""
    SEQUENTIAL = "sequential"  # Agents run one after another
    PARALLEL = "parallel"      # Agents run simultaneously
    LOOP = "loop"              # Agents run in a loop until condition met
    
    @classmethod
    def normalize(cls, pattern: Any) -> 'AgentPattern':
        """Normalize a pattern input to an AgentPattern enum"""
        # Direct enum match
        if isinstance(pattern, cls):
            return pattern
        
        # String matching
        if isinstance(pattern, str):
            pattern_lower = pattern.lower().strip()
            if pattern_lower in ["sequential", "seq"]:
                return cls.SEQUENTIAL
            elif pattern_lower in ["parallel", "par"]:
                return cls.PARALLEL
            elif pattern_lower in ["loop", "looping"]:
                return cls.LOOP
            # Check for enum string representation
            if "SEQUENTIAL" in pattern.upper():
                return cls.SEQUENTIAL
            elif "PARALLEL" in pattern.upper():
                return cls.PARALLEL
            elif "LOOP" in pattern.upper():
                return cls.LOOP
        
        # Try to extract from object
        if hasattr(pattern, 'value'):
            pattern_val = pattern.value
            if pattern_val == cls.SEQUENTIAL.value:
                return cls.SEQUENTIAL
            elif pattern_val == cls.PARALLEL.value:
                return cls.PARALLEL
            elif pattern_val == cls.LOOP.value:
                return cls.LOOP
        
        # Try string representation
        pattern_str = str(pattern)
        if "SEQUENTIAL" in pattern_str.upper():
            return cls.SEQUENTIAL
        elif "PARALLEL" in pattern_str.upper():
            return cls.PARALLEL
        elif "LOOP" in pattern_str.upper():
            return cls.LOOP
        
        # Default to SEQUENTIAL if unknown
        return cls.SEQUENTIAL


class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents with different execution patterns
    Supports sequential, parallel, and loop patterns
    """
    
    def __init__(self, session_service: InMemorySessionService):
        self.agents: Dict[str, BaseAgent] = {}
        self.session_service = session_service
        self.logger = logging.getLogger("orchestrator")
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.agent_id}")
    
    def register_agents(self, agents: List[BaseAgent]):
        """Register multiple agents"""
        for agent in agents:
            self.register_agent(agent)
    
    def execute_sequential(
        self,
        agents: List[str],
        initial_message: AgentMessage,
        context: AgentContext
    ) -> List[AgentMessage]:
        """
        Execute agents sequentially (one after another)
        Each agent receives the previous agent's output
        """
        self.logger.info(f"Executing sequential pattern with agents: {agents}")
        
        messages = [initial_message]
        current_message = initial_message
        
        for agent_id in agents:
            if agent_id not in self.agents:
                self.logger.warning(f"Agent {agent_id} not found, skipping")
                continue
            
            agent = self.agents[agent_id]
            
            # Create message from previous agent's output
            agent_message = AgentMessage(
                sender=current_message.sender,
                receiver=agent_id,
                content=current_message.content,
                metadata=current_message.metadata,
                session_id=context.session_id
            )
            
            # Process with agent
            response = agent.process(agent_message, context)
            messages.append(response)
            current_message = response
        
        return messages
    
    def execute_parallel(
        self,
        agents: List[str],
        initial_message: AgentMessage,
        context: AgentContext
    ) -> Dict[str, AgentMessage]:
        """
        Execute agents in parallel (simultaneously)
        All agents receive the same input message
        """
        self.logger.info(f"Executing parallel pattern with agents: {agents}")
        
        results = {}
        
        # Create tasks for parallel execution
        tasks = []
        for agent_id in agents:
            if agent_id not in self.agents:
                self.logger.warning(f"Agent {agent_id} not found, skipping")
                continue
            
            agent = self.agents[agent_id]
            agent_message = AgentMessage(
                sender=initial_message.sender,
                receiver=agent_id,
                content=initial_message.content,
                metadata=initial_message.metadata,
                session_id=context.session_id
            )
            
            # Execute agent (synchronous for now, can be made async)
            try:
                response = agent.process(agent_message, context)
                results[agent_id] = response
            except Exception as e:
                self.logger.error(f"Error in agent {agent_id}: {e}")
                results[agent_id] = AgentMessage(
                    sender=agent_id,
                    receiver=initial_message.sender,
                    content=f"Error: {str(e)}",
                    session_id=context.session_id
                )
        
        return results
    
    def execute_loop(
        self,
        agents: List[str],
        initial_message: AgentMessage,
        context: AgentContext,
        condition: Callable[[List[AgentMessage]], bool],
        max_iterations: int = 10
    ) -> List[AgentMessage]:
        """
        Execute agents in a loop until condition is met
        Agents run sequentially in each iteration
        """
        self.logger.info(f"Executing loop pattern with agents: {agents}, max_iterations: {max_iterations}")
        
        messages = [initial_message]
        current_message = initial_message
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            self.logger.debug(f"Loop iteration {iteration}")
            
            # Execute agents sequentially in this iteration
            iteration_messages = []
            for agent_id in agents:
                if agent_id not in self.agents:
                    continue
                
                agent = self.agents[agent_id]
                agent_message = AgentMessage(
                    sender=current_message.sender,
                    receiver=agent_id,
                    content=current_message.content,
                    metadata=current_message.metadata,
                    session_id=context.session_id
                )
                
                response = agent.process(agent_message, context)
                iteration_messages.append(response)
                current_message = response
            
            messages.extend(iteration_messages)
            
            # Check condition
            if condition(iteration_messages):
                self.logger.info(f"Loop condition met at iteration {iteration}")
                break
        
        if iteration >= max_iterations:
            self.logger.warning(f"Loop reached max iterations: {max_iterations}")
        
        return messages
    
    def route_message(
        self,
        message: AgentMessage,
        context: AgentContext,
        pattern: AgentPattern = AgentPattern.SEQUENTIAL,
        agent_ids: Optional[List[str]] = None
    ) -> Any:
        """
        Route message to agents based on pattern
        """
        if agent_ids is None:
            # Auto-route based on message content
            agent_ids = self._auto_route(message.content)
        
        # Normalize pattern using the helper method
        try:
            normalized_pattern = AgentPattern.normalize(pattern)
        except Exception as e:
            self.logger.error(f"Error normalizing pattern {pattern}: {e}")
            # Fallback: try to extract pattern from string
            pattern_str = str(pattern).upper()
            if "SEQUENTIAL" in pattern_str:
                normalized_pattern = AgentPattern.SEQUENTIAL
            elif "PARALLEL" in pattern_str:
                normalized_pattern = AgentPattern.PARALLEL
            elif "LOOP" in pattern_str:
                normalized_pattern = AgentPattern.LOOP
            else:
                # Default to SEQUENTIAL
                normalized_pattern = AgentPattern.SEQUENTIAL
                self.logger.warning(f"Could not determine pattern from {pattern}, defaulting to SEQUENTIAL")
        
        # Execute based on normalized pattern
        if normalized_pattern == AgentPattern.SEQUENTIAL:
            return self.execute_sequential(agent_ids, message, context)
        elif normalized_pattern == AgentPattern.PARALLEL:
            return self.execute_parallel(agent_ids, message, context)
        elif normalized_pattern == AgentPattern.LOOP:
            condition = lambda msgs: any("complete" in msg.content.lower() or "done" in msg.content.lower() 
                                         for msg in msgs)
            return self.execute_loop(agent_ids, message, context, condition)
        else:
            # This should never happen, but just in case
            error_msg = f"Unknown normalized pattern: {normalized_pattern} (original: {pattern})"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def _auto_route(self, message_content: str) -> List[str]:
        """Auto-route message to appropriate agents based on content"""
        content_lower = message_content.lower()
        
        # Determine which agents to use
        agents = []
        
        if any(keyword in content_lower for keyword in ['crop', 'recommend', 'plant', 'grow']):
            agents.append("crop_agent")
        
        if any(keyword in content_lower for keyword in ['disease', 'leaf', 'pest', 'detect']):
            agents.append("disease_agent")
        
        # Always include chat agent as fallback
        if not agents:
            agents.append("chat_agent")
        else:
            agents.append("chat_agent")  # Add chat agent for final response formatting
        
        return agents
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all registered agents"""
        return {
            agent_id: agent.get_state()
            for agent_id, agent in self.agents.items()
        }

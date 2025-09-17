"""
Agent implementation for {{ project_name }}.

This module contains the core agent classes and related functionality.
"""

import asyncio
import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable

from .exceptions import AgentError, CommunicationError


class AgentStatus(Enum):
    """Agent status enumeration."""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class ResourceLimits:
    """Resource limits for an agent."""
    max_memory: int  # in MB
    max_cpu: float   # as percentage
    max_connections: int
    max_processing_time: float  # in seconds


@dataclass
class RetryPolicy:
    """Retry policy for failed operations."""
    max_attempts: int = 3
    base_delay: float = 1.0  # in seconds
    max_delay: float = 60.0  # in seconds
    exponential_base: float = 2.0
    jitter: bool = True


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    agent_id: str
    agent_type: str
    settings: Dict[str, Any]
    dependencies: List[str]
    resources: ResourceLimits
    retry_policy: RetryPolicy
    timeout: Optional[float] = None


class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, config: AgentConfig) -> None:
        """Initialize the agent with configuration."""
        self.config = config
        self.agent_id = config.agent_id
        self.agent_type = config.agent_type
        self.status = AgentStatus.INITIALIZING
        self.logger = logging.getLogger(f"agent.{self.agent_id}")
        self.message_handlers: Dict[str, Callable] = {}
        self._running = False
        self._tasks: List[asyncio.Task] = []
        
        # Register default message handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self) -> None:
        """Register default message handlers."""
        self.message_handlers.update({
            "heartbeat": self._handle_heartbeat,
            "status": self._handle_status_request,
            "shutdown": self._handle_shutdown_request,
        })
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the agent with required resources."""
        pass
    
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process an incoming message."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully shutdown the agent."""
        pass
    
    async def start(self) -> None:
        """Start the agent."""
        try:
            self.logger.info(f"Starting agent {self.agent_id}")
            self.status = AgentStatus.INITIALIZING
            
            # Initialize the agent
            await self.initialize()
            
            # Start the main processing loop
            self.status = AgentStatus.RUNNING
            self._running = True
            
            # Start background tasks
            self._tasks.append(asyncio.create_task(self._main_loop()))
            self._tasks.append(asyncio.create_task(self._heartbeat_loop()))
            
            self.logger.info(f"Agent {self.agent_id} started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start agent {self.agent_id}: {e}")
            self.status = AgentStatus.ERROR
            raise AgentError(f"Failed to start agent: {e}") from e
    
    async def stop(self) -> None:
        """Stop the agent."""
        try:
            self.logger.info(f"Stopping agent {self.agent_id}")
            self.status = AgentStatus.STOPPING
            self._running = False
            
            # Cancel all tasks
            for task in self._tasks:
                task.cancel()
            
            # Wait for tasks to complete
            if self._tasks:
                await asyncio.gather(*self._tasks, return_exceptions=True)
            
            # Shutdown the agent
            await self.shutdown()
            
            self.status = AgentStatus.STOPPED
            self.logger.info(f"Agent {self.agent_id} stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping agent {self.agent_id}: {e}")
            self.status = AgentStatus.ERROR
            raise AgentError(f"Error stopping agent: {e}") from e
    
    async def _main_loop(self) -> None:
        """Main processing loop for the agent."""
        while self._running:
            try:
                # This would typically process messages from a queue
                # For now, just sleep to prevent busy waiting
                await asyncio.sleep(0.1)
                
            except asyncio.CancelledError:
                self.logger.info(f"Main loop cancelled for agent {self.agent_id}")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop for agent {self.agent_id}: {e}")
                self.status = AgentStatus.ERROR
                break
    
    async def _heartbeat_loop(self) -> None:
        """Send periodic heartbeat messages."""
        while self._running:
            try:
                await asyncio.sleep(10.0)  # Send heartbeat every 10 seconds
                
                if self._running:
                    await self._send_heartbeat()
                    
            except asyncio.CancelledError:
                self.logger.info(f"Heartbeat loop cancelled for agent {self.agent_id}")
                break
            except Exception as e:
                self.logger.error(f"Error in heartbeat loop for agent {self.agent_id}: {e}")
    
    async def _send_heartbeat(self) -> None:
        """Send a heartbeat message."""
        # This would typically send a message to a message broker
        # For now, just log the heartbeat
        self.logger.debug(f"Heartbeat from agent {self.agent_id}")
    
    async def _handle_heartbeat(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle heartbeat messages."""
        return {
            "status": "ok",
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_status_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle status request messages."""
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "agent_type": self.agent_type,
            "uptime": "not_implemented",  # Would calculate actual uptime
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_shutdown_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle shutdown request messages."""
        self.logger.info(f"Received shutdown request for agent {self.agent_id}")
        await self.stop()
        return {
            "status": "shutdown_complete",
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def register_handler(self, message_type: str, handler: Callable) -> None:
        """Register a message handler for a specific message type."""
        self.message_handlers[message_type] = handler
        self.logger.debug(f"Registered handler for message type: {message_type}")
    
    async def send_message(self, recipient: str, message_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to another agent."""
        # This would typically send a message through a message broker
        # For now, just log the message
        self.logger.debug(f"Sending {message_type} message to {recipient}")
        
        # Simulate message processing
        return {
            "status": "sent",
            "message_id": str(uuid.uuid4()),
            "recipient": recipient,
            "timestamp": datetime.now().isoformat()
        }


class AgentManager:
    """Manages the lifecycle of all agents in the system."""
    
    def __init__(self, config: "SystemConfig") -> None:
        """Initialize the agent manager."""
        self.config = config
        self.logger = logging.getLogger("agent_manager")
        self.agents: Dict[str, BaseAgent] = {}
        self._running = False
    
    async def start(self) -> None:
        """Start the agent manager and all agents."""
        self.logger.info("Starting agent manager")
        self._running = True
        
        # Start all registered agents
        for agent in self.agents.values():
            await agent.start()
        
        self.logger.info("Agent manager started successfully")
    
    async def stop(self) -> None:
        """Stop the agent manager and all agents."""
        self.logger.info("Stopping agent manager")
        self._running = False
        
        # Stop all agents
        for agent in self.agents.values():
            await agent.stop()
        
        self.logger.info("Agent manager stopped")
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the manager."""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.agent_id}")
    
    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent from the manager."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.logger.info(f"Unregistered agent: {agent_id}")
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID."""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[str]:
        """List all registered agent IDs."""
        return list(self.agents.keys())


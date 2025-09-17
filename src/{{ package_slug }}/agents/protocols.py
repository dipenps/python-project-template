"""
Agent communication protocols for {{ project_name }}.

This module defines the protocols and interfaces for agent communication.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class MessageType(Enum):
    """Types of messages between agents."""
    COMMAND = "command"
    EVENT = "event"
    QUERY = "query"
    RESPONSE = "response"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


@dataclass
class AgentMessage:
    """Message sent between agents."""
    id: str
    type: MessageType
    sender: str
    recipient: str
    timestamp: datetime
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Post-initialization processing."""
        if isinstance(self.type, str):
            self.type = MessageType(self.type)
        
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))


@dataclass
class AgentResponse:
    """Response from an agent."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata or {},
            "processing_time": self.processing_time,
            "timestamp": self.timestamp.isoformat()
        }


class AgentProtocol(ABC):
    """Base protocol for all agents."""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the agent."""
        pass
    
    @abstractmethod
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process an incoming message."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully shutdown the agent."""
        pass
    
    @abstractmethod
    async def send_message(self, recipient: str, message_type: MessageType, payload: Dict[str, Any]) -> AgentResponse:
        """Send a message to another agent."""
        pass
    
    @abstractmethod
    async def broadcast_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Broadcast an event to all interested agents."""
        pass
    
    @abstractmethod
    async def query_agent(self, agent_id: str, query: Dict[str, Any]) -> AgentResponse:
        """Query another agent for information."""
        pass


class MessageHandler(ABC):
    """Base class for message handlers."""
    
    @abstractmethod
    async def handle(self, message: AgentMessage) -> AgentResponse:
        """Handle a message."""
        pass
    
    @abstractmethod
    def can_handle(self, message_type: MessageType) -> bool:
        """Check if this handler can handle a message type."""
        pass


class EventSubscriber(ABC):
    """Base class for event subscribers."""
    
    @abstractmethod
    async def on_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle an event."""
        pass
    
    @abstractmethod
    def get_subscribed_events(self) -> list[str]:
        """Get list of event types this subscriber is interested in."""
        pass


class CommandHandler(MessageHandler):
    """Handler for command messages."""
    
    async def handle(self, message: AgentMessage) -> AgentResponse:
        """Handle a command message."""
        if message.type != MessageType.COMMAND:
            return AgentResponse(
                success=False,
                error=f"Expected command message, got {message.type.value}"
            )
        
        # Process the command
        return await self.process_command(message.payload)
    
    def can_handle(self, message_type: MessageType) -> bool:
        """Check if this handler can handle command messages."""
        return message_type == MessageType.COMMAND
    
    @abstractmethod
    async def process_command(self, payload: Dict[str, Any]) -> AgentResponse:
        """Process a command payload."""
        pass


class QueryHandler(MessageHandler):
    """Handler for query messages."""
    
    async def handle(self, message: AgentMessage) -> AgentResponse:
        """Handle a query message."""
        if message.type != MessageType.QUERY:
            return AgentResponse(
                success=False,
                error=f"Expected query message, got {message.type.value}"
            )
        
        # Process the query
        return await self.process_query(message.payload)
    
    def can_handle(self, message_type: MessageType) -> bool:
        """Check if this handler can handle query messages."""
        return message_type == MessageType.QUERY
    
    @abstractmethod
    async def process_query(self, payload: Dict[str, Any]) -> AgentResponse:
        """Process a query payload."""
        pass


class EventHandler(MessageHandler):
    """Handler for event messages."""
    
    async def handle(self, message: AgentMessage) -> AgentResponse:
        """Handle an event message."""
        if message.type != MessageType.EVENT:
            return AgentResponse(
                success=False,
                error=f"Expected event message, got {message.type.value}"
            )
        
        # Process the event
        await self.process_event(message.payload)
        
        return AgentResponse(success=True)
    
    def can_handle(self, message_type: MessageType) -> bool:
        """Check if this handler can handle event messages."""
        return message_type == MessageType.EVENT
    
    @abstractmethod
    async def process_event(self, payload: Dict[str, Any]) -> None:
        """Process an event payload."""
        pass


class HeartbeatHandler(MessageHandler):
    """Handler for heartbeat messages."""
    
    async def handle(self, message: AgentMessage) -> AgentResponse:
        """Handle a heartbeat message."""
        if message.type != MessageType.HEARTBEAT:
            return AgentResponse(
                success=False,
                error=f"Expected heartbeat message, got {message.type.value}"
            )
        
        # Process the heartbeat
        return await self.process_heartbeat(message.payload)
    
    def can_handle(self, message_type: MessageType) -> bool:
        """Check if this handler can handle heartbeat messages."""
        return message_type == MessageType.HEARTBEAT
    
    @abstractmethod
    async def process_heartbeat(self, payload: Dict[str, Any]) -> AgentResponse:
        """Process a heartbeat payload."""
        pass


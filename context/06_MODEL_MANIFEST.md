# Model Manifest

## Model Overview

This document describes the models, schemas, and data structures used in the {{ project_name }} system.

## Core Models

### Agent Models

#### BaseAgent
```python
class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    agent_id: str
    agent_type: str
    status: AgentStatus
    config: AgentConfig
    message_handlers: Dict[str, Callable]
    
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
```

#### AgentStatus
```python
class AgentStatus(Enum):
    """Agent status enumeration."""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
```

#### AgentConfig
```python
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
```

### Message Models

#### AgentMessage
```python
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
```

#### MessageType
```python
class MessageType(Enum):
    """Types of messages between agents."""
    COMMAND = "command"
    EVENT = "event"
    QUERY = "query"
    RESPONSE = "response"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
```

#### AgentResponse
```python
@dataclass
class AgentResponse:
    """Response from an agent."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
```

### Resource Models

#### ResourceLimits
```python
@dataclass
class ResourceLimits:
    """Resource limits for an agent."""
    max_memory: int  # in MB
    max_cpu: float   # as percentage
    max_connections: int
    max_processing_time: float  # in seconds
```

#### RetryPolicy
```python
@dataclass
class RetryPolicy:
    """Retry policy for failed operations."""
    max_attempts: int = 3
    base_delay: float = 1.0  # in seconds
    max_delay: float = 60.0  # in seconds
    exponential_base: float = 2.0
    jitter: bool = True
```

### Processing Models

#### ProcessingTask
```python
@dataclass
class ProcessingTask:
    """A task to be processed by an agent."""
    task_id: str
    agent_id: str
    task_type: str
    input_data: Any
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    timeout: Optional[float] = None
```

#### ProcessingResult
```python
@dataclass
class ProcessingResult:
    """Result of processing a task."""
    task_id: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    processing_time: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
    completed_at: datetime = field(default_factory=datetime.now)
```

### Configuration Models

#### SystemConfig
```python
@dataclass
class SystemConfig:
    """System-wide configuration."""
    log_level: str = "INFO"
    max_agents: int = 100
    message_timeout: float = 30.0
    heartbeat_interval: float = 10.0
    cleanup_interval: float = 300.0
    data_dir: str = "./data"
    log_dir: str = "./logs"
```

#### AgentRegistry
```python
@dataclass
class AgentRegistry:
    """Registry of available agents."""
    agents: Dict[str, AgentInfo]
    last_updated: datetime = field(default_factory=datetime.now)
    
@dataclass
class AgentInfo:
    """Information about a registered agent."""
    agent_id: str
    agent_type: str
    version: str
    status: AgentStatus
    capabilities: List[str]
    dependencies: List[str]
```

## Data Schemas

### JSON Schema Definitions

#### Agent Message Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-zA-Z0-9_-]+$"
    },
    "type": {
      "type": "string",
      "enum": ["command", "event", "query", "response", "error", "heartbeat"]
    },
    "sender": {
      "type": "string",
      "minLength": 1,
      "maxLength": 50
    },
    "recipient": {
      "type": "string",
      "minLength": 1,
      "maxLength": 50
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "payload": {
      "type": "object"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "required": ["id", "type", "sender", "recipient", "timestamp", "payload"]
}
```

#### Agent Config Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "agent_id": {
      "type": "string",
      "pattern": "^[a-zA-Z0-9_-]+$"
    },
    "agent_type": {
      "type": "string",
      "minLength": 1
    },
    "settings": {
      "type": "object",
      "additionalProperties": true
    },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "resources": {
      "type": "object",
      "properties": {
        "max_memory": {
          "type": "integer",
          "minimum": 1
        },
        "max_cpu": {
          "type": "number",
          "minimum": 0.1,
          "maximum": 100.0
        },
        "max_connections": {
          "type": "integer",
          "minimum": 1
        },
        "max_processing_time": {
          "type": "number",
          "minimum": 0.1
        }
      },
      "required": ["max_memory", "max_cpu", "max_connections", "max_processing_time"]
    }
  },
  "required": ["agent_id", "agent_type", "settings", "dependencies", "resources"]
}
```

## Model Validation

### Validation Rules
- **Type Safety**: All models use type hints and dataclasses
- **Schema Validation**: JSON schema validation for serialized data
- **Business Rules**: Custom validation for business logic
- **Range Validation**: Numeric values within valid ranges

### Validation Functions
```python
def validate_agent_message(message: AgentMessage) -> bool:
    """Validate an agent message."""
    # Check required fields
    # Validate data types
    # Check business rules
    return True

def validate_agent_config(config: AgentConfig) -> bool:
    """Validate agent configuration."""
    # Check configuration values
    # Validate resource limits
    # Check dependencies
    return True
```

## Model Serialization

### JSON Serialization
```python
def serialize_agent_message(message: AgentMessage) -> str:
    """Serialize agent message to JSON."""
    return json.dumps(asdict(message), default=str)

def deserialize_agent_message(data: str) -> AgentMessage:
    """Deserialize JSON to agent message."""
    return AgentMessage(**json.loads(data))
```

### YAML Serialization
```python
def serialize_agent_config(config: AgentConfig) -> str:
    """Serialize agent config to YAML."""
    return yaml.dump(asdict(config), default_flow_style=False)

def deserialize_agent_config(data: str) -> AgentConfig:
    """Deserialize YAML to agent config."""
    return AgentConfig(**yaml.safe_load(data))
```

## Model Evolution

### Versioning Strategy
- **Backward Compatibility**: Maintain compatibility for at least 2 major versions
- **Migration Scripts**: Provide migration scripts for breaking changes
- **Deprecation Warnings**: Warn about deprecated fields and methods
- **Documentation**: Document all changes and migration paths

### Change Management
- **Schema Versioning**: Include version in all schemas
- **Field Deprecation**: Mark deprecated fields clearly
- **Breaking Changes**: Major version bumps for breaking changes
- **Testing**: Comprehensive testing for model changes


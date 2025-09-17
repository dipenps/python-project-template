# Protocol Documentation

## Agent Communication Protocol

This document defines the communication protocols used by agents in the {{ project_name }} system.

## Message Format

### Base Message Structure
```json
{
  "id": "unique-message-id",
  "type": "message-type",
  "sender": "agent-id",
  "recipient": "agent-id",
  "timestamp": "2024-01-01T00:00:00Z",
  "payload": {
    "data": "message-content"
  },
  "metadata": {
    "priority": "normal",
    "ttl": 3600,
    "correlation_id": "request-id"
  }
}
```

### Message Types

#### 1. Command Messages
Used for direct instructions between agents.

```json
{
  "type": "command",
  "payload": {
    "action": "process_data",
    "parameters": {
      "input_file": "path/to/file",
      "output_format": "json"
    }
  }
}
```

#### 2. Event Messages
Used for broadcasting state changes or notifications.

```json
{
  "type": "event",
  "payload": {
    "event_type": "data_processed",
    "data": {
      "file_path": "path/to/file",
      "status": "completed",
      "result_count": 1000
    }
  }
}
```

#### 3. Query Messages
Used for requesting information from other agents.

```json
{
  "type": "query",
  "payload": {
    "query_type": "status",
    "parameters": {
      "agent_id": "target-agent"
    }
  }
}
```

#### 4. Response Messages
Used for responding to queries or commands.

```json
{
  "type": "response",
  "payload": {
    "status": "success",
    "data": {
      "result": "query-result"
    }
  }
}
```

## Agent Lifecycle

### 1. Initialization Phase
```python
async def initialize(self) -> None:
    """Initialize the agent with required resources."""
    # Load configuration
    # Set up connections
    # Register message handlers
    # Start background tasks
```

### 2. Running Phase
```python
async def run(self) -> None:
    """Main agent execution loop."""
    while self.is_running:
        # Process incoming messages
        # Execute scheduled tasks
        # Update internal state
        # Send outgoing messages
```

### 3. Shutdown Phase
```python
async def shutdown(self) -> None:
    """Gracefully shutdown the agent."""
    # Stop accepting new messages
    # Complete current operations
    # Clean up resources
    # Send shutdown notifications
```

## Communication Patterns

### 1. Request-Response
- Synchronous communication pattern
- Used for immediate responses
- Timeout handling required

### 2. Publish-Subscribe
- Asynchronous communication pattern
- Used for event broadcasting
- Multiple subscribers supported

### 3. Message Queue
- Reliable message delivery
- Used for critical operations
- Persistence and retry mechanisms

## Error Handling

### Error Response Format
```json
{
  "type": "error",
  "payload": {
    "error_code": "AGENT_ERROR",
    "error_message": "Human-readable error message",
    "error_details": {
      "exception_type": "ValueError",
      "stack_trace": "..."
    }
  }
}
```

### Retry Policy
- Maximum 3 retry attempts
- Exponential backoff (1s, 2s, 4s)
- Dead letter queue for failed messages

## Security

### Message Authentication
- Digital signatures for message integrity
- Timestamp validation for replay protection
- Agent identity verification

### Message Encryption
- TLS for transport security
- End-to-end encryption for sensitive data
- Key rotation support

## Performance Considerations

### Message Size Limits
- Maximum message size: 1MB
- Large data should use external storage
- Reference IDs for large payloads

### Rate Limiting
- Maximum 100 messages per second per agent
- Burst allowance for critical messages
- Backpressure handling

## Monitoring

### Message Metrics
- Message throughput per agent
- Message latency distribution
- Error rate by message type
- Queue depth monitoring

### Health Checks
- Agent availability status
- Message processing rate
- Resource utilization
- Error frequency


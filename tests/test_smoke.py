"""
Smoke tests for {{ project_name }}.

These tests verify that the basic functionality works without errors.
"""

import pytest
from my_package.core import SystemConfig, AgentStatus
from my_package.agents.protocols import MessageType, AgentMessage
from my_package.utils.validation import validate_agent_message, validate_agent_config
from click.testing import CliRunner

from {{ package_slug }}.cli import cli


class TestSystemConfig:
    """Test system configuration functionality."""
    
    def test_default_config(self) -> None:
        """Test default configuration creation."""
        config = SystemConfig()
        assert config.log_level == "INFO"
        assert config.max_agents == 100
        assert config.message_timeout == 30.0
        assert config.heartbeat_interval == 10.0
        assert config.cleanup_interval == 300.0
        assert config.debug is False
    
    def test_config_validation(self) -> None:
        """Test configuration validation."""
        config = SystemConfig()
        config.validate()  # Should not raise
        
        # Test invalid configuration
        config.max_agents = -1
        with pytest.raises(ValueError, match="max_agents must be positive"):
            config.validate()
    
    def test_config_to_dict(self) -> None:
        """Test configuration to dictionary conversion."""
        config = SystemConfig()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "log_level" in config_dict
        assert "max_agents" in config_dict
        assert "message_timeout" in config_dict


class TestAgentStatus:
    """Test agent status enumeration."""
    
    def test_agent_status_values(self) -> None:
        """Test agent status values."""
        assert AgentStatus.INITIALIZING.value == "initializing"
        assert AgentStatus.RUNNING.value == "running"
        assert AgentStatus.PAUSED.value == "paused"
        assert AgentStatus.STOPPING.value == "stopping"
        assert AgentStatus.STOPPED.value == "stopped"
        assert AgentStatus.ERROR.value == "error"


class TestMessageType:
    """Test message type enumeration."""
    
    def test_message_type_values(self) -> None:
        """Test message type values."""
        assert MessageType.COMMAND.value == "command"
        assert MessageType.EVENT.value == "event"
        assert MessageType.QUERY.value == "query"
        assert MessageType.RESPONSE.value == "response"
        assert MessageType.ERROR.value == "error"
        assert MessageType.HEARTBEAT.value == "heartbeat"


class TestAgentMessage:
    """Test agent message functionality."""
    
    def test_agent_message_creation(self) -> None:
        """Test agent message creation."""
        message = AgentMessage(
            id="test-123",
            type=MessageType.COMMAND,
            sender="agent-a",
            recipient="agent-b",
            timestamp="2024-01-01T00:00:00Z",
            payload={"action": "test"}
        )
        
        assert message.id == "test-123"
        assert message.type == MessageType.COMMAND
        assert message.sender == "agent-a"
        assert message.recipient == "agent-b"
        assert message.payload == {"action": "test"}
    
    def test_agent_message_string_timestamp(self) -> None:
        """Test agent message with string timestamp."""
        message = AgentMessage(
            id="test-123",
            type="command",  # String type
            sender="agent-a",
            recipient="agent-b",
            timestamp="2024-01-01T00:00:00Z",  # String timestamp
            payload={"action": "test"}
        )
        
        assert message.type == MessageType.COMMAND
        assert isinstance(message.timestamp, str)


class TestValidation:
    """Test validation functionality."""
    
    def test_validate_agent_message_valid(self) -> None:
        """Test valid agent message validation."""
        message = {
            "id": "test-123",
            "type": "command",
            "sender": "agent-a",
            "recipient": "agent-b",
            "timestamp": "2024-01-01T00:00:00Z",
            "payload": {"action": "test"}
        }
        
        assert validate_agent_message(message) is True
    
    def test_validate_agent_message_invalid(self) -> None:
        """Test invalid agent message validation."""
        # Missing required field
        message = {
            "id": "test-123",
            "type": "command",
            "sender": "agent-a",
            "recipient": "agent-b",
            "payload": {"action": "test"}
        }
        
        assert validate_agent_message(message) is False
    
    def test_validate_agent_config_valid(self) -> None:
        """Test valid agent configuration validation."""
        config = {
            "agent_id": "test-agent",
            "agent_type": "test",
            "settings": {"key": "value"},
            "dependencies": ["dep1", "dep2"],
            "resources": {
                "max_memory": 512,
                "max_cpu": 50.0,
                "max_connections": 10,
                "max_processing_time": 30.0
            }
        }
        
        assert validate_agent_config(config) is True
    
    def test_validate_agent_config_invalid(self) -> None:
        """Test invalid agent configuration validation."""
        # Missing required field
        config = {
            "agent_id": "test-agent",
            "agent_type": "test",
            "settings": {"key": "value"},
            "dependencies": ["dep1", "dep2"]
        }
        
        assert validate_agent_config(config) is False


class TestSmokeTests:
    """Test basic smoke tests."""
    
    def test_import_package(self) -> None:
        """Test that the package can be imported."""
        import my_package
        assert hasattr(my_package, "__version__")
        assert hasattr(my_package, "__author__")
        assert hasattr(my_package, "__email__")
    
    def test_import_core_modules(self) -> None:
        """Test that core modules can be imported."""
        from my_package.core import BaseAgent, AgentStatus, AgentConfig
        from my_package.agents.protocols import AgentProtocol, MessageType
        from my_package.utils import load_config, setup_logging
        
        # Just test that imports work
        assert BaseAgent is not None
        assert AgentStatus is not None
        assert AgentConfig is not None
        assert AgentProtocol is not None
        assert MessageType is not None
        assert load_config is not None
        assert setup_logging is not None
    
    def test_basic_functionality(self) -> None:
        """Test basic functionality without errors."""
        # Test configuration creation
        config = SystemConfig()
        assert config is not None
        
        # Test message type
        message_type = MessageType.COMMAND
        assert message_type is not None
        
        # Test validation
        valid_message = {
            "id": "test",
            "type": "command",
            "sender": "a",
            "recipient": "b",
            "timestamp": "2024-01-01T00:00:00Z",
            "payload": {}
        }
        assert validate_agent_message(valid_message) is True


def test_cli_version():
    """Test the CLI's version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "{{ project_name }} version" in result.output

def test_cli_help():
    """Test the CLI's help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in result.output


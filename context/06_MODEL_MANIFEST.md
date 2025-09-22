# Model Manifest

## Model Overview

This document describes the primary data models, schemas, and data structures used in {{ project_name }}, managed with Pydantic for type safety and validation.

## Core Models

### Settings Model
The `Settings` model defines the application's configuration.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Defines application settings, loaded from .env files or environment variables."""
    PROJECT_NAME: str = "{{ project_name }}"
    LOG_LEVEL: str = "INFO"
    # Add other settings like database URLs, API keys, etc.
    # DATABASE_URL: str = "sqlite:///./default.db"
```

### Data Processing Models

These models define the structure of data as it moves through a processing pipeline.

#### Input Data Schema
```python
from pydantic import BaseModel, Field

class InputData(BaseModel):
    """
    Schema for input data records. Ensures that incoming data
    conforms to the expected structure and types.
    """
    record_id: str
    value_to_process: float
    category: str
    is_valid: bool = Field(default=True, description="Flag for data quality checks.")
```

#### Output Data Schema
```python
class OutputData(BaseModel):
    """
    Schema for processed data records. This can include results,
    predictions, or transformed values.
    """
    record_id: str
    processed_value: float
    status: str = "SUCCESS"
```

### Task and Result Models

For more complex pipelines, you can define tasks and their results.

#### Processing Task
```python
from typing import Any

class ProcessingTask(BaseModel):
    """Represents a single task to be executed by a pipeline."""
    task_id: str
    task_type: str
    input_data: Any
    priority: int = 0
```

#### Processing Result
```python
class ProcessingResult(BaseModel):
    """Represents the result of a completed task."""
    task_id: str
    success: bool
    result: Any | None = None
    error: str | None = None
    processing_time_seconds: float
```

## Data Schemas

Pydantic models serve as the primary source of truth for data schemas. They can be exported to JSON Schema if needed for external systems.

### Generating JSON Schema
```python
import json

schema = InputData.model_json_schema()
print(json.dumps(schema, indent=2))
```

## Model Validation

Validation is handled automatically by Pydantic when creating model instances.

### Validation Example
```python
from pydantic import ValidationError

# Valid data
valid_data = {"record_id": "A123", "value_to_process": 99.5, "category": "X"}
try:
    input_record = InputData(**valid_data)
    print("Validation successful!")
except ValidationError as e:
    print(f"This should not happen: {e}")

# Invalid data (missing required field)
invalid_data = {"record_id": "B456", "category": "Y"}
try:
    input_record = InputData(**invalid_data)
except ValidationError as e:
    print(f"Validation failed as expected:\\n{e}")

```

## Model Serialization

Pydantic provides built-in methods for serialization to and from dictionaries and JSON.

### JSON Serialization
```python
output = OutputData(record_id="A123", processed_value=199.0)

# Serialize to JSON string
json_output = output.model_dump_json()

# Deserialize from JSON string
deserialized_output = OutputData.model_validate_json(json_output)
```

## Model Evolution

### Versioning Strategy
- For significant changes to a model that are not backward-compatible, consider creating a new version of the model (e.g., `InputDataV2`).
- Use tools like `alembic` for database schema migrations if models are persisted.

### Change Management
- Document all model changes in the project's changelog.
- Ensure tests are updated to reflect model modifications.


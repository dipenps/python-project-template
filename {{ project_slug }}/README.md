# {{ project_name }}

{{ description }}

## Quick Start

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Prerequisites

- Python {{ python_version }} or later
- [uv](https://github.com/astral-sh/uv) installed

### Installation

```bash
# Clone the repository
git clone https://github.com/{{ github_username }}/{{ project_slug }}.git
cd {{ project_slug }}

# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Development

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run mypy .

# Format code
uv run ruff format .
```

## Project Structure

```
{{ project_slug }}/
├── src/{{ package_slug }}/          # Main package source code
│   ├── core/                        # Core business logic
│   ├── utils/                       # Utility functions
│   └── agents/                      # Agent-based components
├── tests/                           # Test suite
├── scripts/                         # Maintenance scripts
├── tools/                           # Development tools
├── docs/                            # Documentation
└── .github/workflows/               # CI/CD workflows
```

## Documentation

- [Project Plan](PLAN.md)
- [Technical Specification](SPEC.md)
- [Protocol Documentation](PROTOCOL.md)
- [Constraints](CONSTRAINTS.md)
- [Data Manifest](DATA_MANIFEST.md)
- [Model Manifest](MODEL_MANIFEST.md)
- [Evaluation Plan](EVAL_PLAN.md)
- [Architecture Decisions](DECISIONS.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Glossary](GLOSSARY.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite and linting
6. Submit a pull request

## License

This project is licensed under the {{ license }} License - see the [LICENSE](LICENSE) file for details.


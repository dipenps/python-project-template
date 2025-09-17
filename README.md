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

# Copy the file to a new project
 uvx copier copy --vcs-ref=main https://github.com/dipenps/python-project-template my-new-project

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

## AI Context

This project includes a `context/` directory with detailed documentation to provide a comprehensive understanding of the project for an AI agent. The files are numbered to suggest a reading order.

- [Technical Specification](context/01_SPEC.md)
- [Project Plan](context/02_PLAN.md)
- [Constraints](context/03_CONSTRAINTS.md)
- [Protocol Documentation](context/04_PROTOCOL.md)
- [Data Manifest](context/05_DATA_MANIFEST.md)
- [Model Manifest](context/06_MODEL_MANIFEST.md)
- [Evaluation Plan](context/07_EVAL_PLAN.md)
- [Glossary](context/08_GLOSSARY.md)
- [Architecture Decisions](context/09_DECISIONS.md)
- [Deployment Guide](context/10_DEPLOYMENT.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite and linting
6. Submit a pull request

## License

This project is licensed under the {{ license }} License - see the [LICENSE](LICENSE) file for details.


# {{ project_name }}

A production-grade Python project template for CLI and data science pipelines.

## Quick Start

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Prerequisites

- Python {{ python_version }} or later
- [uv](https://github.com/astral-sh/uv) installed
- [copier](https://copier.readthedocs.io/en/stable/) installed (`uvx pip install copier`)

### Installation

To create a new project from this template, run:

```bash
# Create a new project
copier copy gh:{{ github_username }}/{{ project_slug }} my-new-project
cd my-new-project

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
│   └── utils/                       # Utility functions
├── tests/                           # Test suite
├── scripts/                         # Maintenance scripts
├── tools/                           # Development tools
├── docs/                            # Documentation
└── .github/workflows/               # CI/CD workflows
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite and linting
6. Submit a pull request

## License

This project is licensed under the {{ license }} License - see the [LICENSE](LICENSE) file for details.


# {{ project_name }} Documentation

Welcome to the {{ project_name }} documentation!

This project provides a production-grade template for building CLI applications and data science pipelines in Python.

## Quick Start

Get started with {{ project_name }} in just a few steps:

1.  **Create a new project from the template:**
    ```bash
    # Make sure you have copier installed: uvx pip install copier
    copier copy gh:{{ github_username }}/{{ project_slug }} my-new-project
    cd my-new-project
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Basic Usage:**
    ```bash
    # Run the application
    uv run {{ package_slug }} --help
    ```

4.  **Development:**
    ```bash
    # Run tests
    uv run pytest

    # Run linting
    uv run ruff check .
    uv run mypy .
    ```

## Features

- **Robust CLI**: Built with Click for a powerful and user-friendly command-line interface.
- **Type Safety**: Comprehensive type hints and mypy integration.
- **Fast Package Management**: Uses uv for fast dependency management.
- **Comprehensive Testing**: pytest for unit and integration testing.
- **Code Quality**: ruff for linting and formatting.
- **Pre-commit Hooks**: Automated code quality checks.
- **CI/CD Ready**: GitHub Actions workflow included.

## Architecture

{{ project_name }} is built with a focus on:

- **Modularity**: Components are designed to be self-contained and reusable.
- **Scalability**: The architecture is designed to scale with your needs.
- **Reliability**: Robust error handling and logging are built-in.

## Documentation Structure

- [Project Plan](PLAN.md) - High-level project planning and milestones
- [Technical Specification](SPEC.md) - Detailed technical requirements
- [Constraints](CONSTRAINTS.md) - System constraints and limitations
- [Data Manifest](DATA_MANIFEST.md) - Data models and schemas
- [Model Manifest](MODEL_MANIFEST.md) - System models and structures
- [Evaluation Plan](EVAL_PLAN.md) - Testing and validation strategy
- [Architecture Decisions](DECISIONS.md) - Key architectural decisions
- [Deployment Guide](DEPLOYMENT.md) - Deployment instructions
- [Glossary](GLOSSARY.md) - Terms and definitions

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite and linting
6. Submit a pull request

## License

This project is licensed under the {{ license }} License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/{{ github_username }}/{{ project_slug }}/issues)
- **Discussions**: [GitHub Discussions](https://github.com/{{ github_username }}/{{ project_slug }}/discussions)
- **Documentation**: [Project Documentation](https://{{ github_username }}.github.io/{{ project_slug }})


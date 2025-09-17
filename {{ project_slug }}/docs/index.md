# {{ project_name }} Documentation

Welcome to the {{ project_name }} documentation!

## Quick Start

Get started with {{ project_name }} in just a few steps:

1. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/{{ github_username }}/{{ project_slug }}.git
   cd {{ project_slug }}
   
   # Install dependencies
   uv sync
   ```

2. **Basic Usage**
   ```bash
   # Run the application
   uv run {{ package_slug }} --help
   
   # Start the agent system
   uv run {{ package_slug }} run
   ```

3. **Development**
   ```bash
   # Run tests
   uv run pytest
   
   # Run linting
   uv run ruff check .
   uv run mypy .
   ```

## Features

- **Agent-Based Architecture**: Modular, scalable agent system
- **Async-First Design**: Built with modern Python async/await patterns
- **Type Safety**: Comprehensive type hints and mypy integration
- **Fast Package Management**: Uses uv for fast dependency management
- **Comprehensive Testing**: pytest with async support and coverage
- **Code Quality**: ruff for linting and formatting
- **Pre-commit Hooks**: Automated code quality checks
- **CI/CD Ready**: GitHub Actions workflow included

## Architecture

{{ project_name }} is built around an agent-based architecture where:

- **Agents** are self-contained components that can process messages
- **Communication** happens through standardized message protocols
- **Scalability** is achieved through horizontal agent scaling
- **Reliability** is ensured through error handling and retry mechanisms

## Documentation Structure

- [Project Plan](PLAN.md) - High-level project planning and milestones
- [Technical Specification](SPEC.md) - Detailed technical requirements
- [Protocol Documentation](PROTOCOL.md) - Agent communication protocols
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


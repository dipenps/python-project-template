python-uv-agent-template/
├── copier.yml                     # Copier template configuration
├── {{ project_slug }}/            # Project root after rendering
│   ├── README.md                  # Project documentation
│   ├── PLAN.md                    # Project planning document
│   ├── TODO.md                    # Task tracking
│   ├── SPEC.md                    # Technical specification
│   ├── PROTOCOL.md                # Agent communication protocols
│   ├── CONSTRAINTS.md             # System constraints
│   ├── DATA_MANIFEST.md           # Data models and schemas
│   ├── MODEL_MANIFEST.md          # System models
│   ├── EVAL_PLAN.md               # Evaluation and testing plan
│   ├── DECISIONS.md               # Architecture decisions
│   ├── DEPLOYMENT.md              # Deployment guide
│   ├── GLOSSARY.md                # Terms and definitions
│   ├── pyproject.toml             # uv project configuration
│   ├── .gitignore                 # Git ignore rules
│   ├── .pre-commit-config.yaml    # Pre-commit hooks
│   ├── .ruff.toml                 # Ruff linting configuration
│   ├── mypy.ini                   # MyPy type checking configuration
│   ├── src/{{ package_slug }}/    # Main package source
│   │   ├── __init__.py
│   │   ├── cli.py                 # Command-line interface
│   │   ├── core/                  # Core business logic
│   │   │   ├── __init__.py
│   │   │   ├── agent.py           # Agent implementation
│   │   │   ├── exceptions.py      # Custom exceptions
│   │   │   └── system.py          # System configuration
│   │   ├── utils/                 # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── config.py          # Configuration utilities
│   │   │   ├── logging.py         # Logging utilities
│   │   │   └── validation.py      # Validation utilities
│   │   └── agents/                # Agent protocols
│   │       ├── __init__.py
│   │       └── protocols.py       # Agent communication protocols
│   ├── tests/                     # Test suite
│   │   └── test_smoke.py          # Smoke tests
│   ├── scripts/                   # Maintenance scripts
│   │   └── bootstrap.sh           # Development setup script
│   ├── tools/                     # Development tools
│   │   └── precommit-msg.sh       # Commit message validation
│   ├── docs/                      # Documentation
│   │   └── index.md               # Main documentation
│   └── .github/workflows/         # CI/CD workflows
│       └── ci.yml                 # GitHub Actions workflow
└── LICENSE                        # License file
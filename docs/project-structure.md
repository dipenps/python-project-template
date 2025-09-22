python-uv-agent-template/
├── copier.yml                     # Copier template configuration at template root
├── README.md                      # Project documentation
├── TODO.md                        # Task tracking
├── context/                       # Project context and specifications
│   ├── 01_SPEC.md                 # Technical specification
│   ├── 02_PLAN.md                 # Project planning document
│   ├── 03_CONSTRAINTS.md          # System constraints
│   ├── 05_DATA_MANIFEST.md        # Data models and schemas
│   ├── 06_MODEL_MANIFEST.md       # System models
│   ├── 07_EVAL_PLAN.md            # Evaluation and testing plan
│   ├── 08_GLOSSARY.md             # Terms and definitions
│   ├── 09_DECISIONS.md            # Architecture decisions
│   └── 10_DEPLOYMENT.md           # Deployment guide
├── pyproject.toml                 # uv project configuration
├── mypy.ini                       # MyPy type checking configuration
├── LICENSE                        # License file
├── project-directory.md           # This file (helper; excluded from copy)
├── docs/                          # Documentation
│   └── index.md                   # Main documentation
├── scripts/                       # Maintenance scripts
│   └── bootstrap.sh               # Development setup script
├── tests/                         # Test suite
│   └── test_smoke.py              # Smoke tests
├── tools/                         # Development tools
│   └── precommit-msg.sh           # Commit message validation
└── src/                           # Source code
    └── [[ package_slug ]] /       # Rendered to the Python package name
        ├── __init__.py
        ├── cli.py                 # Command-line interface
        ├── core/                  # Core business logic
        │   ├── __init__.py
        │   ├── exceptions.py      # Custom exceptions
        │   └── system.py          # System configuration and settings
        └── utils/                 # Utility functions
            ├── __init__.py
            └── logging.py         # Logging utilities

# Notes:
# - This template is root-based; no subdirectory indirection is used.
# - The placeholder [[ package_slug ]] is resolved from answers at render time.
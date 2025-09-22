#!/bin/bash
# Bootstrap script for {{ project_name }}
# This script sets up the development environment

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if uv is installed
check_uv() {
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Please install uv first."
        print_status "Installation instructions: https://github.com/astral-sh/uv#installation"
        exit 1
    fi
    print_success "uv is installed"
}

# Check Python version
check_python() {
    local python_version
    python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    local major_version
    major_version=$(echo "$python_version" | cut -d'.' -f1)
    local minor_version
    minor_version=$(echo "$python_version" | cut -d'.' -f2)
    
    if [ "$major_version" -lt 3 ] || [ "$major_version" -eq 3 ] && [ "$minor_version" -lt 11 ]; then
        print_error "Python {{ python_version }} or later is required. Found: $python_version"
        exit 1
    fi
    print_success "Python version check passed: $python_version"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies with uv..."
    uv sync --dev
    print_success "Dependencies installed"
}

# Set up pre-commit hooks
setup_pre_commit() {
    print_status "Setting up pre-commit hooks..."
    uv run pre-commit install
    print_success "Pre-commit hooks installed"
}

# Run initial tests
run_tests() {
    print_status "Running initial tests..."
    uv run pytest tests/ -v
    print_success "Tests passed"
}

# Run linting
run_linting() {
    print_status "Running linting..."
    uv run ruff check .
    uv run mypy .
    print_success "Linting passed"
}

# Main function
main() {
    print_status "Bootstrapping {{ project_name }} development environment..."
    
    check_uv
    check_python
    install_dependencies
    setup_pre_commit
    run_tests
    run_linting
    
    print_success "Bootstrap completed successfully!"
    print_status "You can now start developing with:"
    print_status "  uv run {{ package_slug }} --help"
    print_status "  uv run pytest"
    print_status "  uv run ruff check ."
    print_status "  uv run mypy ."
}

# Run main function
main "$@"


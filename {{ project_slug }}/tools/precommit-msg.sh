#!/bin/bash
# Pre-commit message hook for {{ project_name }}
# This script validates commit messages

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Get the commit message
commit_msg_file="$1"
commit_msg=$(cat "$commit_msg_file")

# Check if commit message is empty
if [ -z "$commit_msg" ]; then
    print_error "Commit message cannot be empty"
    exit 1
fi

# Check commit message format
# Format: type(scope): description
# Types: feat, fix, docs, style, refactor, test, chore
# Examples:
#   feat: add new feature
#   fix(api): resolve authentication issue
#   docs: update README
#   style: format code with black
#   refactor: simplify agent communication
#   test: add unit tests for validation
#   chore: update dependencies

if ! echo "$commit_msg" | grep -qE '^(feat|fix|docs|style|refactor|test|chore)(\([a-zA-Z0-9_-]+\))?: .+'; then
    print_error "Invalid commit message format"
    print_error "Expected format: type(scope): description"
    print_error "Types: feat, fix, docs, style, refactor, test, chore"
    print_error "Example: feat(api): add new authentication endpoint"
    exit 1
fi

# Check message length
if [ ${#commit_msg} -gt 100 ]; then
    print_warning "Commit message is longer than 100 characters"
    print_warning "Consider using a shorter description"
fi

# Check for common issues
if echo "$commit_msg" | grep -qi "wip\|work in progress\|todo\|fixme"; then
    print_warning "Commit message contains WIP/TODO/FIXME keywords"
    print_warning "Consider if this commit is ready to be merged"
fi

print_success "Commit message validation passed"
exit 0


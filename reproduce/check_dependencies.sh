#!/bin/bash
# check_dependencies.sh - Verify required tools are available
#
# Checks for uv, Python 3.12+, and optionally jq (for benchmark viewing).
# Meant to be sourced or called early in reproduce.sh / reproduce_min.sh.

set -e

ERRORS=0

check_cmd() {
    local cmd="$1"
    local install_hint="$2"
    if command -v "$cmd" &> /dev/null; then
        echo "  [OK] $cmd: $(command -v "$cmd")"
    else
        echo "  [MISSING] $cmd -- $install_hint" >&2
        ERRORS=$((ERRORS + 1))
    fi
}

echo "Checking dependencies..."
echo ""

# Python
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
    PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
    if [[ "$PY_MAJOR" -ge 3 && "$PY_MINOR" -ge 12 ]]; then
        echo "  [OK] python3: $PY_VERSION"
    else
        echo "  [WARN] python3: $PY_VERSION (3.12+ recommended)" >&2
    fi
else
    echo "  [MISSING] python3 -- install Python 3.12+" >&2
    ERRORS=$((ERRORS + 1))
fi

# uv
check_cmd "uv" "install with: curl -LsSf https://astral.sh/uv/install.sh | sh"

# git
check_cmd "git" "install git from https://git-scm.com/"

# jq (optional, for benchmark viewing)
if command -v jq &> /dev/null; then
    echo "  [OK] jq: $(jq --version 2>/dev/null || echo 'available')"
else
    echo "  [INFO] jq not found (optional, needed for benchmark_results.sh)"
fi

echo ""

if [[ "$ERRORS" -gt 0 ]]; then
    echo "$ERRORS required dependency(ies) missing. Please install them and retry."
    exit 1
else
    echo "All required dependencies found."
fi

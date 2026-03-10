#!/bin/bash
# Life-Cycle-Prime-Time REMARK - Minimal Reproduction Script
#
# Quick validation (<5 minutes) that the environment is correct and
# the estimation code runs. The REMARK cli.py prefers this script
# over reproduce.sh when it exists.
#
# What this validates:
#   1. Dependencies install correctly
#   2. The estimark package imports and its version is consistent
#   3. A single low-resource estimation completes successfully
#
# For full reproduction of all results, run reproduce.sh instead.

set -e

echo "=========================================="
echo "Life-Cycle-Prime-Time - Quick Validation"
echo "=========================================="
echo ""

# Ensure we are in the repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Ensure uv is available and install dependencies
echo "Step 1/3: Installing dependencies..."
if ! command -v uv &> /dev/null; then
    echo "  uv not found, installing..."
    pip install "uv>=0.5,<1.0"
fi
echo "  uv $(uv --version)"
uv sync
echo "  Dependencies installed."
echo ""

# Step 2: Run the test suite
echo "Step 2/3: Running test suite..."
uv run pytest tests/test_package.py -v
echo ""

# Step 3: Run a single low-resource estimation (~90 seconds)
echo "Step 3/3: Running single low-resource estimation..."
uv run python -c "
from estimark.min import estimate_min
from estimark.options import low_resource
estimate_min(**low_resource)
print('Low-resource estimation completed successfully.')
"
echo ""

echo "=========================================="
echo "Quick validation complete!"
echo "=========================================="

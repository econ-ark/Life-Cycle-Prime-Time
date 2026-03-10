#!/bin/bash
# Life-Cycle-Prime-Time REMARK - Full Reproduction Script
#
# This script reproduces all results in the repository.
# It works in all three REMARK execution contexts:
#   1. Docker container (via Dockerfile)
#   2. Binder (via binder/environment.yml + postBuild)
#   3. REMARK cli.py conda path (via conda env update + this script)
#
# Dependencies are managed via pyproject.toml + uv.lock using uv.

set -e

echo "=========================================="
echo "Life-Cycle-Prime-Time - Full Reproduction"
echo "=========================================="
echo ""

# Ensure we are in the repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Ensure uv is available
echo "Step 1/2: Installing dependencies..."
if ! command -v uv &> /dev/null; then
    echo "  uv not found, installing..."
    pip install "uv>=0.5,<1.0"
fi
echo "  uv $(uv --version)"

# Install/sync all dependencies from pyproject.toml + uv.lock
uv sync
echo "  Dependencies installed."
echo ""

# Step 2: Run the full reproduction
echo "Step 2/2: Running full estimation (3 agent models)..."
echo "  This may take a long time depending on hardware."
echo ""
uv run python src/run_all.py

echo ""
echo "=========================================="
echo "Reproduction complete!"
echo "=========================================="

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
#
# On success, a benchmark JSON is written to reproduce/benchmarks/results/
# capturing system characteristics and timing. See reproduce/README.md.

set -eo pipefail

# Ensure we are in the repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
cd "$SCRIPT_DIR"

# Source shared utilities (logging, error handling, benchmarking)
# shellcheck source=reproduce/reproduce_utils.sh
source "$SCRIPT_DIR/reproduce/reproduce_utils.sh"

init_logging "full"
benchmark_start "full"

echo "=========================================="
echo "Life-Cycle-Prime-Time - Full Reproduction"
echo "=========================================="
echo ""

# Step 1: Ensure uv is available
log STEP "Step 1/2: Installing dependencies..."
if ! command -v uv &> /dev/null; then
    log INFO "uv not found, installing..."
    pip install "uv>=0.5,<1.0"
fi
log INFO "uv $(uv --version)"

uv sync
log SUCCESS "Dependencies installed."
echo ""

# Step 2: Run the full reproduction
log STEP "Step 2/2: Running full estimation (3 agent models)..."
log INFO "This may take a long time depending on hardware."
echo ""
uv run python src/run_all.py

log SUCCESS "All estimations completed."

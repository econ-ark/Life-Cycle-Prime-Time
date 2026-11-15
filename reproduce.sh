#!/bin/bash
# Life-Cycle-Prime-Time REMARK - Full Reproduction Script
#
# This script reproduces the paper's table of estimated parameters
# (docs/parameters.tex): it repeats the three estimations behind it as they were
# run, and prints the results beside the paper's (see reproduce/paper_table.py).
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
    pip install "uv==0.8.13"
fi
log INFO "uv $(uv --version)"

uv sync --locked
use_optimagic_copy_of_estimagic
log SUCCESS "Dependencies installed."
echo ""

# Step 2: Reproduce the paper's table of estimated parameters
log STEP "Step 2/2: Reproducing the paper's estimates (3 models)..."
echo ""
uv run python reproduce/paper_table.py

log SUCCESS "All estimations completed."

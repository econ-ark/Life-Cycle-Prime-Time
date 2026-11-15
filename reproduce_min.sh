#!/bin/bash
# Life-Cycle-Prime-Time REMARK - Minimal Reproduction Script
#
# Quick validation (a few minutes) that the environment is correct and
# reproduces the paper. The REMARK cli.py prefers this script over
# reproduce.sh when it exists.
#
# What this validates:
#   1. Dependencies install correctly
#   2. The estimark package imports and its version is consistent
#   3. The paper's Life-Cycle Portfolio estimate is reproduced (the first
#      row of docs/parameters.tex; see reproduce/paper_table.py)
#
# On success, a benchmark JSON is written to reproduce/benchmarks/results/
# capturing system characteristics and timing. See reproduce/README.md.
#
# For full reproduction of all results, run reproduce.sh instead.

set -eo pipefail

# Ensure we are in the repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
cd "$SCRIPT_DIR"

# Source shared utilities (logging, error handling, benchmarking)
# shellcheck source=reproduce/reproduce_utils.sh
source "$SCRIPT_DIR/reproduce/reproduce_utils.sh"

init_logging "min"
benchmark_start "min"

echo "=========================================="
echo "Life-Cycle-Prime-Time - Quick Validation"
echo "=========================================="
echo ""

# Step 1: Ensure uv is available and install dependencies
log STEP "Step 1/3: Installing dependencies..."
if ! command -v uv &> /dev/null; then
    log INFO "uv not found, installing..."
    pip install "uv==0.8.13"
fi
log INFO "uv $(uv --version)"
uv sync --locked --extra test   # pytest, for step 2, is in the test extra
use_optimagic_copy_of_estimagic
log SUCCESS "Dependencies installed."
echo ""

# Step 2: Run the test suite
log STEP "Step 2/3: Running test suite..."
uv run pytest tests/test_package.py -v
log SUCCESS "Tests passed."
echo ""

# Step 3: Reproduce the paper's Life-Cycle Portfolio estimate (a few minutes)
log STEP "Step 3/3: Reproducing the paper's Life-Cycle Portfolio estimate..."
uv run python reproduce/paper_table.py --models PortfolioG

log SUCCESS "Quick validation completed."

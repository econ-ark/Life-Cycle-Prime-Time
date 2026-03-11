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
    pip install "uv>=0.5,<1.0"
fi
log INFO "uv $(uv --version)"
uv sync
log SUCCESS "Dependencies installed."
echo ""

# Step 2: Run the test suite
log STEP "Step 2/3: Running test suite..."
uv run pytest tests/test_package.py -v
log SUCCESS "Tests passed."
echo ""

# Step 3: Run a single low-resource estimation (~90 seconds)
log STEP "Step 3/3: Running single low-resource estimation (Portfolio model)..."
uv run python -c "
from estimark.estimation import estimate
from estimark.options import low_resource

specs = low_resource.copy()
specs['agent_name'] = 'Portfolio'
specs['save_dir'] = 'docs/tables/TRP'
print('Model:', specs['agent_name'])
estimate(**specs)
print('Low-resource estimation completed successfully.')
"

log SUCCESS "Quick validation completed."

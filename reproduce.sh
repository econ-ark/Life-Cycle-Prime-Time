#!/bin/bash
# Life-Cycle-Prime-Time REMARK reproduction script
# This script reproduces all results in the repository

set -e  # Exit on any error

echo "=========================================="
echo "Life-Cycle-Prime-Time - Full Reproduction"
echo "=========================================="
echo ""

# Detect workspace directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
WORKSPACE_DIR="$SCRIPT_DIR"

# Check if setup script exists and use it, otherwise fall back to conda
if [ -f "$WORKSPACE_DIR/reproduce/docker/setup.sh" ]; then
    echo "Step 1/3: Setting up environment using setup script..."
    bash "$WORKSPACE_DIR/reproduce/docker/setup.sh"
    
    # Activate the platform-specific venv
    ARCH=$(uname -m)
    PLATFORM=""
    case "$(uname -s)" in
        Darwin) PLATFORM="darwin" ;;
        Linux) PLATFORM="linux" ;;
        *) PLATFORM="linux" ;;  # Default fallback
    esac
    VENV_PATH="$WORKSPACE_DIR/.venv-$PLATFORM-$ARCH"
    
    if [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
        export PYTHONPATH="$WORKSPACE_DIR/src:$PYTHONPATH"
        echo "✓ Environment activated: $VENV_PATH"
    else
        echo "⚠️ Warning: Expected venv not found at $VENV_PATH"
        echo "Attempting to use uv run instead..."
    fi
    echo ""
    
    echo "Step 2/3: Running reproduction script..."
    if command -v uv &> /dev/null && [ -f "$WORKSPACE_DIR/pyproject.toml" ]; then
        cd "$WORKSPACE_DIR"
        uv run ipython src/run_all.py
    else
        python src/run_all.py
    fi
    
elif command -v conda >/dev/null 2>&1; then
    echo "Step 1/3: Setting up conda environment..."
    # Check if the environment exists
    if conda env list | grep -q 'life-cycle-prime-time'; then
        echo "Environment 'life-cycle-prime-time' already exists. Updating it..."
        conda env update -q -f binder/environment.yml
    else
        echo "Creating environment using conda..."
        conda env create -q -f binder/environment.yml
    fi
    
    # Activate the environment
    eval "$(conda shell.bash hook)"
    conda activate life-cycle-prime-time
    
    echo ""
    echo "Step 2/3: Running postBuild script to install dependencies..."
    if [ -f "$WORKSPACE_DIR/binder/postBuild" ]; then
        bash "$WORKSPACE_DIR/binder/postBuild"
    fi
    
    echo ""
    echo "Step 3/3: Running reproduction script..."
    ipython src/run_all.py
else
    echo "❌ Neither setup script nor conda found."
    echo "Please install conda or ensure reproduce/docker/setup.sh exists."
    exit 1
fi

echo ""
echo "=========================================="
echo "Reproduction complete!"
echo "=========================================="

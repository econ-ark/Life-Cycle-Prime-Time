#!/bin/bash

# Life-Cycle-Prime-Time REMARK reproduction script
# This script reproduces all results in the repository

set -e  # Exit on any error

# Check if conda is available
if ! command -v conda >/dev/null 2>&1; then
    echo "Conda is not available. Please install Anaconda or Miniconda."
    exit 1
fi

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

# Execute script to reproduce figures
echo "Running reproduction script..."
ipython src/run_all.py

echo "Reproduction complete!"

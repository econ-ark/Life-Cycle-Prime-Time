#!/bin/bash

# Check if conda is available
if ! command -v conda >/dev/null 2>&1; then
    echo "Conda is not available. Please install Anaconda or Miniconda."
    exit 1
fi

# Check if the environment exists
if conda env list | grep -q 'estimatingmicrodsops'; then
    echo "Environment 'estimatingmicrodsops' already exists. Updating it..."
    conda env update -q -f environment.yml
else
    echo "Creating environment using conda..."
    conda env create -q -f environment.yml
fi

# Activate the environment
conda activate estimatingmicrodsops

# Execute script to reproduce figures
ipython src/run_all.py

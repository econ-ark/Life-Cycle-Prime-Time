# Life-Cycle-Prime-Time

A reproducible research repository for life-cycle portfolio choice models with method of simulated moments (MSM) estimation.

**Documentation**: https://econ-ark.github.io/Life-Cycle-Prime-Time/

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/econ-ark/Life-Cycle-Prime-Time/HEAD)

## Overview

This repository contains code, data, and documentation to reproduce results for life-cycle consumption and portfolio choice models. The project uses method of simulated moments (MSM) estimation to match model predictions with empirical data from the Survey of Consumer Finances.

## Key Features

- Life-cycle consumption and portfolio choice models
- Method of simulated moments (MSM) estimation
- Sensitivity analysis and parameter estimation
- Portfolio share functions and consumption functions
- Reproducible research environment with Docker and Binder support

## Installation

To reproduce all the results in the repository, first clone this repository locally:

```bash
# Clone this repository
$ git clone https://github.com/econ-ark/Life-Cycle-Prime-Time

# Change working directory to Life-Cycle-Prime-Time
$ cd Life-Cycle-Prime-Time
```

## Reproduction Methods

You can reproduce results using either a local conda environment or Docker-based tools:

### Method 1: Local Conda Environment

Create a conda environment and execute the reproduction script:

```bash
$ conda env create -f binder/environment.yml
$ conda activate life-cycle-prime-time
$ bash reproduce.sh
```

Alternatively, you can run the main script directly:

```bash
$ conda activate life-cycle-prime-time
$ python src/do_all.py
```

### Method 2: Docker (Recommended for Reproducibility)

Use Docker to run the reproduction in a containerized environment:

```bash
$ docker build -t life-cycle-prime-time .
$ docker run -it life-cycle-prime-time bash reproduce.sh
```

### Method 3: nbreproduce (Requires Docker)

Use the `nbreproduce` tool for automated reproduction:

```bash
# Install nbreproduce
$ pip install nbreproduce

# Reproduce all results using nbreproduce
$ nbreproduce
```

### Method 4: Binder

Click the Binder badge above to launch an interactive environment in your browser.

## Project Structure

```
Life-Cycle-Prime-Time/
├── binder/
│   └── environment.yml      # Conda environment specification
├── docs/                    # Documentation and results
│   ├── figures/            # Generated figures
│   └── tables/             # Generated tables
├── src/                     # Source code
│   ├── estimark/           # Main estimation package
│   ├── notebooks/          # Jupyter notebooks
│   └── run_all.py          # Main reproduction script
├── Dockerfile              # Docker container definition
├── reproduce.sh            # Reproduction script
└── README.md               # This file
```

## Requirements

- Python 3.12
- See `binder/environment.yml` for complete dependency list
- Key dependencies:
  - econ-ark/HARK (from GitHub master branch)
  - estimagic==0.4.7
  - statsmodels
  - dask
  - openpyxl

## Outputs

Running the reproduction script generates:
- Figures in `docs/figures/` (PDF, PNG, SVG formats)
- Tables in `docs/tables/` (CSV format)
- Model estimation results and parameter estimates

## REMARK Compliance

This repository complies with REMARK (Reproducible Explorations Made using ARK) standards:

- **Tier**: 2 (Reproducible REMARK)
- Dockerfile for containerized execution
- `reproduce.sh` script for automated reproduction
- `binder/environment.yml` for reproducible environments
- Comprehensive documentation

See `REMARK.md` for detailed metadata and compliance information.

## References

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/econ-ark/Life-Cycle-Prime-Time/workflows/CI/badge.svg
[actions-link]:             https://github.com/econ-ark/Life-Cycle-Prime-Time/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/estimark
[conda-link]:               https://github.com/conda-forge/estimark-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/econ-ark/Life-Cycle-Prime-Time/discussions
[pypi-link]:                https://pypi.org/project/estimark/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/estimark
[pypi-version]:             https://img.shields.io/pypi/v/estimark
[rtd-badge]:                https://readthedocs.org/projects/estimark/badge/?version=latest
[rtd-link]:                 https://estimark.readthedocs.io/en/latest/?badge=latest

<!-- prettier-ignore-end -->

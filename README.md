# Life-Cycle-Prime-Time

A reproducible research repository for life-cycle consumption and portfolio
choice models estimated via the method of simulated moments (MSM).

**Documentation**: https://econ-ark.github.io/Life-Cycle-Prime-Time/

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/econ-ark/Life-Cycle-Prime-Time/HEAD)

## Overview

This repository contains code, data, and documentation to reproduce results
for life-cycle consumption and portfolio choice models. The project uses the
method of simulated moments (MSM) to estimate model parameters by matching
model predictions with empirical data from the Survey of Consumer Finances.

Three model variants are estimated:

- **Portfolio** -- life-cycle portfolio choice
- **WealthPortfolio** -- portfolio model with wealth-in-utility
- **WarmGlowPortfolio** -- portfolio model with warm-glow bequest motive

## Key Features

- Life-cycle consumption and portfolio choice models
- Method of simulated moments (MSM) estimation
- Sensitivity analysis and parameter estimation
- Portfolio share functions and consumption functions
- Reproducible research environment with Docker and Binder support

## Installation

Clone this repository:

```bash
git clone https://github.com/econ-ark/Life-Cycle-Prime-Time
cd Life-Cycle-Prime-Time
```

## Reproduction

### Quick Validation (< 5 minutes)

```bash
bash reproduce_min.sh
```

This runs the test suite and a single low-resource estimation to verify
the environment is correctly configured.

### Full Reproduction

```bash
bash reproduce.sh
```

This runs MSM estimation for all three agent models and generates all
result tables.

Both scripts use [uv](https://docs.astral.sh/uv/) to manage dependencies
from `pyproject.toml` and `uv.lock`. If `uv` is not already installed, the
scripts will install it automatically.

### Docker (Recommended for Reproducibility)

Build and run the reproduction in a containerized environment:

```bash
docker build -t life-cycle-prime-time .
docker run -it --rm life-cycle-prime-time bash reproduce_min.sh
docker run -it --rm life-cycle-prime-time bash reproduce.sh
```

### Binder

Click the Binder badge above to launch an interactive environment in your
browser for exploring the notebooks.

## Reproduction Time

| Script | What it does | Estimated time |
|---|---|---|
| `reproduce_min.sh` | Test suite + single low-resource estimation | < 3 minutes |
| `reproduce.sh` | Full MSM estimation for 3 agent models | 5--10 minutes |

Reference machine for timing estimates: Intel Core i7-4700MQ @ 2.40GHz,
8GB RAM, Ubuntu 14.04. Modern hardware should be comparable or faster.

The `medium_resource` and `high_resource` settings in `src/estimark/options.py`
take approximately 7 minutes and 1+ hours respectively.

## Project Structure

```
Life-Cycle-Prime-Time/
├── binder/
│   ├── environment.yml      # Minimal conda env (Python 3.12 + uv)
│   ├── postBuild            # Binder dependency installer
│   └── apt.txt              # System dependencies
├── docs/                    # Documentation and results
│   ├── tables/              # Generated estimation tables
│   └── manual_latex_edit_version/  # Manuscript source
├── src/                     # Source code
│   ├── estimark/            # Main estimation package
│   ├── notebooks/           # Jupyter notebooks
│   ├── msm_notebooks/       # MSM-specific notebooks
│   └── run_all.py           # Main reproduction entry point
├── tests/                   # Test suite
├── reproduce/
│   └── docker/
│       └── setup.sh         # Docker environment setup
├── Dockerfile               # Docker container definition
├── reproduce.sh             # Full reproduction script
├── reproduce_min.sh         # Quick validation script
├── pyproject.toml           # Python package configuration
├── uv.lock                  # Locked dependency versions
├── CITATION.cff             # Citation metadata
├── REMARK.md                # REMARK tier and metadata
├── LICENSE                  # MIT license
└── README.md                # This file
```

## Requirements

- Python 3.12
- Dependencies managed via `pyproject.toml` + `uv.lock`
- Key dependencies:
  - [econ-ark/HARK](https://github.com/econ-ark/HARK) (from GitHub master branch)
  - estimagic==0.4.7
  - statsmodels
  - dask
  - openpyxl

## Outputs

Running the full reproduction script generates:

- Estimation result tables in `docs/tables/TRP/`
- Model parameter estimates for each agent variant

Interactive Jupyter notebooks in `src/notebooks/` and `src/msm_notebooks/`
allow exploration of the estimation results.

## REMARK Compliance

This repository complies with [REMARK](https://github.com/econ-ark/REMARK)
(Reproducible Explorations Made using ARK) standards:

- **Tier**: 2 (Reproducible REMARK)
- Dockerfile for containerized execution
- `reproduce.sh` and `reproduce_min.sh` for automated reproduction
- `binder/environment.yml` for Binder and REMARK cli.py compatibility
- `CITATION.cff` for citation metadata
- `REMARK.md` for REMARK tier and project metadata

See [REMARK.md](REMARK.md) for detailed metadata.

## Authors

- Christopher D. Carroll (Johns Hopkins University)
- Alan Lujan (Johns Hopkins University)
- Matthew N. White (Econ-ARK)

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

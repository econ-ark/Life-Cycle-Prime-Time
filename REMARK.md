# REMARK Metadata

- **Tier**: 3 (Published REMARK)
- **Type**: Reproduction
- **Archived**: Zenodo DOI (see CITATION.cff); tag `v0.1.0`

## Project Information

- **Title**: Life-Cycle-Prime-Time
- **Authors**: Christopher D. Carroll, Alan Lujan, Matthew N. White
- **Repository**: https://github.com/econ-ark/Life-Cycle-Prime-Time
- **Documentation**: https://econ-ark.github.io/Life-Cycle-Prime-Time/
- **License**: MIT

## Abstract

This REMARK reproduces results for life-cycle consumption and portfolio
choice models estimated via the method of simulated moments (MSM). It uses
the Econ-ARK/HARK toolkit to solve and estimate dynamic stochastic
optimization problems with heterogeneous agents.

## Models Estimated

The full reproduction (`reproduce.sh`) estimates three agent model variants:

1. **Portfolio** -- life-cycle portfolio choice model
2. **WealthPortfolio** -- portfolio model with wealth-in-utility
3. **WarmGlowPortfolio** -- portfolio model with warm-glow bequest motive

Each model is estimated using MSM with low-resource settings by default.

## Reproduction

### Full Reproduction (`reproduce.sh`)

Runs MSM estimation for all three agent models and generates all tables.

```bash
bash reproduce.sh
```

**Estimated runtime**: The `low_resource` setting takes approximately 20
seconds per agent model on a 2014-era laptop (Intel Core i7-4700MQ @ 2.40GHz,
8GB RAM, Ubuntu 14.04). Total runtime for all three models: approximately
20--60 minutes on modern hardware, longer with higher-resource settings.

### Quick Validation (`reproduce_min.sh`)

Runs the test suite and a single low-resource estimation to verify the
environment is correctly configured.

```bash
bash reproduce_min.sh
```

**Estimated runtime**: Under 25 minutes on modern hardware.

## Environment

- **Python**: 3.12
- **Package manager**: uv (installed via `binder/environment.yml`)
- **Dependencies**: Defined in `pyproject.toml`, locked in `uv.lock`
- **Key packages**: econ-ark/HARK, estimagic==0.4.7, statsmodels, dask, openpyxl

## Outputs

The reproduction generates:

- **Tables**: `docs/tables/TRP/` -- estimation results for each agent model
- **Notebooks**: `src/notebooks/` and `src/msm_notebooks/` -- interactive
  exploration of results
- **Benchmarks**: `reproduce/benchmarks/results/` -- JSON files capturing
  timing, system characteristics, package versions, and git state for each
  successful run. See `reproduce/README.md` for details.

## File Structure

```
.
|-- Dockerfile              # Docker container definition
|-- reproduce.sh            # Full reproduction script
|-- reproduce_min.sh        # Quick validation script
|-- reproduce/
|   |-- README.md           # Reproduction infrastructure docs
|   |-- reproduce_utils.sh  # Shared logging, error handling, benchmarking
|   |-- capture_system_info.py  # System info capture
|   |-- check_dependencies.sh   # Dependency verification
|   |-- logs/               # Timestamped run logs (gitignored)
|   |-- benchmarks/         # Benchmark results and tooling
|   `-- docker/
|       `-- setup.sh        # Docker environment setup
|-- README.md               # Project documentation
|-- LICENSE                 # MIT license
|-- CITATION.cff            # Citation metadata
|-- REMARK.md               # This file
|-- pyproject.toml          # Python package configuration
|-- uv.lock                 # Locked dependency versions
`-- binder/
    |-- environment.yml     # Minimal conda env (Python 3.12 + uv)
    |-- postBuild           # Binder dependency installation script
    `-- apt.txt             # System dependencies
```

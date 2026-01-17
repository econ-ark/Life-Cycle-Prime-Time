# REMARK Metadata

**Tier**: 2 (Reproducible REMARK)

## Project Information

- **Title**: Life-Cycle-Prime-Time
- **Purpose**: Reproducible research repository for life-cycle portfolio choice models with method of simulated moments estimation
- **Repository**: https://github.com/econ-ark/Life-Cycle-Prime-Time
- **Documentation**: https://econ-ark.github.io/Life-Cycle-Prime-Time/

## Authors

- Alan Lujan (alanlujan91@gmail.com)
- Matthew N. White

## Key Components

This REMARK reproduces results for:
- Life-cycle consumption and portfolio choice models
- Method of simulated moments (MSM) estimation
- Sensitivity analysis and parameter estimation
- Portfolio share functions and consumption functions

## Reproduction

All results can be reproduced by running:

```bash
bash reproduce.sh
```

This script:
1. Creates/updates the conda environment from `binder/environment.yml`
2. Executes the main reproduction script `src/run_all.py`

## Environment Requirements

- Python 3.12
- See `binder/environment.yml` for complete dependency list
- Key dependencies: econ-ark/HARK, estimagic, statsmodels, dask

## Outputs

The reproduction script generates:
- Figures in `docs/figures/`
- Tables in `docs/tables/`
- Model estimation results

## Notes

- Full reproduction may take significant time depending on hardware
- The repository includes notebooks in `src/notebooks/` for interactive exploration

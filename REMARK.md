# REMARK Metadata

- **Tier**: 2 (Reproducible REMARK)
- **Type**: Reproduction

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

`reproduce.sh` reproduces the paper's table of estimated parameters,
`docs/parameters.tex`. Each row of the table is one model:

| Row of the table | Run | Parameters estimated |
|---|---|---|
| Life-Cycle Portfolio | `PortfolioG` | CRRA |
| Warm-Glow LC Portfolio | `WarmGlowPortfolioG` | CRRA, bequest MPC (`BeqMPC`), bequest intercept (`BeqInt`) |
| TRP / WIUF LC Portfolio | `WealthPortfolioG` | CRRA, wealth share (`WealthShare`) |

The table's estimates were made on 2025-09-04 (commit `1c581b5`). That run's
output is committed in `src/estimark/docs/tables/min/`, one file per model
(`<run>_estimate_results.csv`). "G" names that run's specification, in which
transitory income shocks continue in retirement.

## Reproduction

### Full reproduction (`reproduce.sh`)

```bash
bash reproduce.sh
```

`reproduce/paper_table.py` repeats the three estimations behind the table as
they were made:

- from the default initial guesses in `src/estimark/parameters.py`, writing
  into an empty folder so that no earlier results file supplies a starting
  point;
- estimating the same parameters;
- with the same multistart exploration sample. The multistart draws its
  sample at random and is not seeded, so a fresh draw would explore different
  points. Each output file records the sample its run drew, and the script
  gives that sample back to the optimizer.

It writes its results to `docs/tables/reproduced/` and prints them beside the
paper's; the comparison is also saved as `docs/tables/reproduced/comparison.csv`.

**Runtime**: 11 minutes (676 seconds) in the REMARK container on an Apple
M4 Max (Docker, linux/arm64, 12 CPUs, 31 GB). The three estimations take
about 2, 6 and 3 minutes.

### Quick validation (`reproduce_min.sh`)

```bash
bash reproduce_min.sh
```

Runs the test suite and reproduces the table's Life-Cycle Portfolio row.

**Runtime**: under 3 minutes (157 seconds) on the same machine.

## Agreement with the Paper

`reproduce.sh` in the REMARK container (the `remark` command-line tool of
econ-ark/REMARK at `2ac99d5`, repo2docker 2026.4.0), beside the run behind the
paper's table:

| Model | Quantity | Paper's table | Run behind the table | Reproduced |
|---|---|---|---|---|
| Life-Cycle Portfolio | CRRA | 9.195 | 9.19534448626031 | 9.19534448626059 |
| | criterion | 1.049 | 1.04900961046565 | 1.04900961046565 |
| Warm-Glow LC Portfolio | CRRA | 4.594 | 4.5942 | 4.6309 |
| | bequest MPC | 0.112 | 0.11185 | 0.11119 |
| | bequest intercept | 0.321 | 0.3210 | 0.3281 |
| | criterion | 0.104 | 0.103988 | 0.104074 |
| TRP / WIUF LC Portfolio | CRRA | 5.136 | 5.1358 | 5.1346 |
| | wealth share | 0.248 | 0.24790 | 0.24798 |
| | criterion | 0.304 | 0.303572 | 0.303574 |

The table's TRP / WIUF criterion read 0.306 until 2026-11-12, a
transcription error: the run behind it recorded 0.3036. The LaTeX sources
are corrected; `docs/life-cycle-prime-time.pdf` and `.docx` still say
0.306 until they are rebuilt.

**What to expect.**

- The Life-Cycle Portfolio estimate reproduces to 13 significant digits.
- On one platform, results are identical from run to run: repeated runs in
  the container gave the same estimates to every digit.
- On another platform, the Warm-Glow and TRP / WIUF estimates can differ from
  the paper's in the third decimal. The runs made in checking this REMARK,
  with the paper's specification, fell within these ranges, the paper's run
  included:

  | Model | Quantity | Range |
  |---|---|---|
  | Warm-Glow LC Portfolio | CRRA | 4.594 to 4.631 |
  | | bequest MPC | 0.1112 to 0.1118 |
  | | bequest intercept | 0.321 to 0.328 |
  | TRP / WIUF LC Portfolio | CRRA | 5.131 to 5.136 |
  | | wealth share | 0.2479 to 0.2484 |
  | Both | criterion | within 0.0001 of the paper's run |

  The paper's text describes the Warm-Glow CRRA as about 4.6, which holds
  throughout.

**Why the third decimal moves.**

- The Warm-Glow and TRP / WIUF objectives are nearly flat near their minima:
  across the ranges above, the criterion changes by less than 0.0001.
- The paper's estimates appear to have been computed on Windows, and the
  container runs Linux. Their math libraries can differ in the last bit of
  functions such as `exp` and `pow`.
- Replaying the recorded samples shows where the runs part:
  - At all 600 recorded exploration points, the objective computed in the
    container matches the recorded values to the 8 digits recorded.
  - The first local search from the best of those points ends about 1e-6 away
    from where the paper's run ended.
  - The multistart, which stops once two local searches agree, then takes a
    different path. For Warm-Glow it stopped after 2 local searches; the
    paper's run made 12.

Not yet run: x86_64 Linux and Windows.

## Environment

- **Python**: 3.12
- **Package manager**: uv 0.8.13 (installed via `binder/environment.yml`)
- **Dependencies**: Defined in `pyproject.toml`, locked in `uv.lock`; the
  versions are those of the lockfile the paper's run used.
- **HARK**: econ-ark/HARK at commit `845fdb5` (2025-07-24)
- **Key packages**: estimagic 0.4.7, optimagic 0.5.2, tranquilo 0.0.5,
  statsmodels, dask, openpyxl
- **estimagic and optimagic**: both install files into the `estimagic`
  package, and which copy of each survives an install varies. The paper's
  run used optimagic's copies, so every environment build reinstalls
  optimagic to make its copies win; see `use_optimagic_copy_of_estimagic`
  in `reproduce/reproduce_utils.sh`.

## Outputs

- **`docs/tables/reproduced/`**: the reproduced estimates, one
  `<run>_estimate_results.csv` per model, and `comparison.csv` (not tracked
  by git).
- **`src/estimark/docs/tables/min/`**: the output of the runs behind the
  paper's table, among other runs.
- **`docs/parameters.tex`**: the paper's table. `docs/tables/parameters.tex`
  is an earlier version (2024).
- **`docs/tables/TRP/`**: output of `src/run_all.py`, which estimates the
  models from whatever results are already in that folder. These are not the
  paper's runs.
- **Notebooks**: `src/notebooks/` and `src/msm_notebooks/`, for interactive
  exploration of results.
- **Benchmarks**: `reproduce/benchmarks/results/`, JSON files capturing
  timing, system characteristics, package versions and git state for each
  successful run. See `reproduce/README.md`.

## File Structure

```
.
|-- Dockerfile              # Docker container definition
|-- reproduce.sh            # Full reproduction script
|-- reproduce_min.sh        # Quick validation script
|-- reproduce/
|   |-- README.md           # Reproduction infrastructure docs
|   |-- paper_table.py      # Repeats the runs behind the paper's table
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

"""Reproduce the paper's table of estimated parameters (docs/parameters.tex).

The table's estimates were made on 2025-09-04 (commit 1c581b5), and that run's outputs
are committed in src/estimark/docs/tables/min/ as <model>G_estimate_results.csv. This
script repeats those runs as they were made:

- from the default initial guesses in estimark/parameters.py: an empty output folder,
  so no earlier results file supplies a starting point;
- estimating the parameters each run estimated;
- with the multistart exploration sample each run drew. The multistart draws its sample
  at random and is not seeded, so a fresh draw would explore different points; each
  output file records its sample, which is read back here and given to the optimizer.

Then it prints the reproduced estimates beside the paper's. On the same platform the
results are identical from run to run. Across platforms they can differ slightly; see
REMARK.md for what to expect and why.

Usage, from the repository root:
    uv run python reproduce/paper_table.py                      # all three models
    uv run python reproduce/paper_table.py --models PortfolioG  # one model
"""

# A command-line script: printing is its output.
# ruff: noqa: T201

from __future__ import annotations

import argparse
import ast
import csv
import shutil
import sys
from pathlib import Path

import estimagic
import optimagic

import estimark.estimation as est
from estimark.options import low_resource

csv.field_size_limit(sys.maxsize)

# The table's rows: the run behind each, and the parameters that run estimated.
MODELS = {
    "PortfolioG": ("Life-Cycle Portfolio", ["CRRA"]),
    "WarmGlowPortfolioG": ("Warm-Glow LC Portfolio", ["CRRA", "BeqMPC", "BeqInt"]),
    "WealthPortfolioG": ("TRP / WIUF LC Portfolio", ["CRRA", "WealthShare"]),
}
PAPER_RUNS = Path("src/estimark/docs/tables/min")


def read_results(path: Path) -> dict[str, str]:
    """An estimate_results.csv as {row name: value}."""
    with path.open(newline="") as f:
        return {
            row[0]: (row[1] if len(row) > 1 else "") for row in csv.reader(f) if row
        }


def recorded_sample(multistart_info: str) -> list[dict[str, float]]:
    """The exploration sample in a MultistartInfo repr, as a list of parameter dicts."""
    start = multistart_info.index("exploration_sample=") + len("exploration_sample=")
    depth = 0
    for end in range(start, len(multistart_info)):
        depth += {"[": 1, "]": -1}.get(multistart_info[end], 0)
        if depth == 0:
            return ast.literal_eval(multistart_info[start : end + 1])
    msg = "no complete exploration_sample in multistart_info"
    raise ValueError(msg)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--models", nargs="+", choices=list(MODELS), default=list(MODELS)
    )
    parser.add_argument("--out", type=Path, default=Path("docs/tables/reproduced"))
    args = parser.parse_args()

    # Only optimagic's estimagic.minimize accepts a given exploration sample, and it is
    # the one the paper's runs used. reproduce/reproduce_utils.sh makes sure it is installed.
    if estimagic.__version__ != optimagic.__version__:
        sys.exit(
            f"estimagic {estimagic.__version__} is not optimagic's copy (optimagic "
            f"{optimagic.__version__}); run this through reproduce.sh or reproduce_min.sh."
        )

    # An empty folder: every run starts from the default initial guess.
    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True)

    base_options = dict(est.minimize_options)
    rows = []
    for name in args.models:
        label, params = MODELS[name]
        paper = read_results(PAPER_RUNS / f"{name}_estimate_results.csv")
        sample = recorded_sample(paper["multistart_info"])
        est.minimize_options = {**base_options, "multistart": {"sample": sample}}

        print(
            f"\n=== {label} ({name}): {len(sample)} recorded exploration points",
            flush=True,
        )
        specs = low_resource.copy()
        specs.update(agent_name=name, params_to_estimate=params, save_dir=str(args.out))
        est.estimate(**specs)

        ours = read_results(args.out / f"{name}_estimate_results.csv")
        for key in [*params, "fun"]:
            p, o = float(paper[key]), float(ours[key])
            rows.append((label, "criterion" if key == "fun" else key, p, o, o - p))
    est.minimize_options = base_options

    with (args.out / "comparison.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["model", "quantity", "paper_run", "reproduced", "difference"])
        writer.writerows(rows)

    print(
        "\nReproduced estimates beside the paper's (the runs behind docs/parameters.tex):\n"
    )
    print(
        f"{'model':26s} {'quantity':12s} {'paper':>14s} {'reproduced':>14s} {'difference':>12s}"
    )
    for label, key, p, o, d in rows:
        print(f"{label:26s} {key:12s} {p:14.6f} {o:14.6f} {d:+12.2e}")
    print(f"\nWritten to {args.out}/. REMARK.md says how closely these should agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

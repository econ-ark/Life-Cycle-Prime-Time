"""Optimization: MSM criterion, estimagic wrappers, bootstrap standard errors."""

from __future__ import annotations

import csv
from time import time

import estimagic as em
import numpy as np
from estimagic.inference import get_bootstrap_samples

from estimark.parameters import (
    age_mapping,
    init_params_options,
    minimize_options,
)
from estimark.scf import scf_data

from .moments import get_weighted_moments
from .simulation import simulate_moments


def msm_criterion(params, agent=None, emp_moments=None, weights=None):
    """The objective function for the SMM estimation.  Given values of discount factor
    adjuster DiscFac, coeffecient of relative risk aversion CRRA, a base consumer
    agent type, empirical data, and calibrated parameters, this function calculates
    the weighted distance between data and the simulated wealth-to-permanent
    income ratio.

    Steps:
        a) solve for consumption functions for (DiscFac, CRRA)
        b) simulate wealth holdings for many consumers over time
        c) sum distances between empirical data and simulated medians within
            seven age groupings

    Parameters
    ----------
    NEED TO WRITE CORRECT INPUTS

    Returns
    -------
    NEED TO WRITE CORRECT OUTPUTS
    """
    emp_moments = emp_moments.copy()
    sim_moments = simulate_moments(params, agent, emp_moments)

    # TODO: make sure all keys in moments have a corresponding
    # key in sim_moments, raise an error if not
    errors = np.array(
        [
            float(weights[key] * (sim_moments[key] - emp_moments[key]))
            for key in emp_moments
        ],
    )

    squared_errors = np.square(errors)
    loss = np.sum(squared_errors)

    return {
        "value": loss,
        "contributions": squared_errors,
        "root_contributions": errors,
    }


def calculate_se_bootstrap(
    agent,
    initial_estimate,
    n_draws=50,
    seed=0,
    verbose=False,
):
    # TODO: WRITE DOCSTRING
    t_0 = time()

    # Generate a list of seeds for generating bootstrap samples
    RNG = np.random.default_rng(seed)

    # Estimate the model N times, recording each set of estimated parameters
    estimate_list = []
    for n in range(n_draws):
        t_start = time()

        # Bootstrap a new dataset by resampling from the original data
        bootstrap_data = get_bootstrap_samples(data=scf_data, rng=RNG)

        # Find moments with bootstrapped sample
        bootstrap_moments, _trash = get_weighted_moments(
            data=bootstrap_data,
            variable="wealth_income_ratio",
            weights="weight",
            groups="age_group",
            mapping=age_mapping,
        )

        # Estimate the model with the bootstrap data and add to list of estimates
        this_estimate = em.minimize(
            msm_criterion,
            initial_estimate,
            criterion_kwargs={"agent": agent, "emp_moments": bootstrap_moments},
            **minimize_options,
        ).params
        estimate_list.append(this_estimate)
        t_now = time()

        if verbose:
            print(
                f"Finished bootstrap estimation #{n + 1} of {n_draws} in {t_now - t_start} seconds ({t_now - t_0} cumulative)",
            )

    # Calculate the standard errors for each parameter
    estimate_array = (np.array(estimate_list)).T
    DiscFac_std_error = np.std(estimate_array[0])
    CRRA_std_error = np.std(estimate_array[1])

    return [DiscFac_std_error, CRRA_std_error]


def _get_bounds(initial_guess):
    """Extract upper/lower bounds for parameters in initial_guess."""
    return {
        bound: {
            k: v for k, v in init_params_options[bound].items() if k in initial_guess
        }
        for bound in ("upper_bounds", "lower_bounds")
    }


def _print_banner(lines):
    """Print centered lines between dashes."""
    width = max(len(line) for line in lines)
    print("-" * width)
    for line in lines:
        print(f"{line:^{width}}")
    print("-" * width)


def estimate_msm(
    agent,
    simulate_moments=None,
    emp_moments=None,
    moments_cov=None,
    initial_params=None,
    minimize_options=None,
    simulate_moments_kwargs=None,
    estimagic_options=None,
):
    # TODO: WRITE DOCSTRING

    t0 = time()

    simulate_moments_kwargs = simulate_moments_kwargs or {}
    simulate_moments_kwargs.setdefault("agent", agent)
    simulate_moments_kwargs.setdefault("emp_moments", emp_moments)

    res = em.estimate_msm(
        simulate_moments,
        emp_moments,
        moments_cov,
        initial_params,
        optimize_options=minimize_options,
        simulate_moments_kwargs=simulate_moments_kwargs,
        **estimagic_options,
    )

    run_time = time() - t0

    return res, run_time


def estimate_min(
    agent,
    criterion=None,
    initial_params=None,
    emp_moments=None,
    minimize_options={},
    criterion_kwargs=None,
    estimagic_options=None,
):
    # TODO: WRITE DOCSTRING

    t0 = time()

    criterion_kwargs = criterion_kwargs or {}
    criterion_kwargs.setdefault("agent", agent)
    criterion_kwargs.setdefault("emp_moments", emp_moments)

    res = em.minimize(
        criterion,
        initial_params,
        criterion_kwargs=criterion_kwargs,
        **minimize_options,
        **estimagic_options,
    )

    run_time = time() - t0

    return res, run_time


_ESTIMATORS = {
    "min": lambda agent,
    initial_guess,
    emp_moments,
    moments_cov,
    minimize_options,
    criterion_kwargs,
    estimagic_options: (
        *estimate_min(
            agent,
            msm_criterion,
            initial_guess,
            emp_moments,
            minimize_options,
            criterion_kwargs=criterion_kwargs,
            estimagic_options=estimagic_options,
        ),
        "params",
    ),
    "msm": lambda agent,
    initial_guess,
    emp_moments,
    moments_cov,
    minimize_options,
    criterion_kwargs,
    estimagic_options: (
        *estimate_msm(
            agent,
            simulate_moments,
            emp_moments,
            moments_cov,
            initial_guess,
            minimize_options,
            estimagic_options=estimagic_options,
        ),
        "_params",
    ),
}


def do_estimate_model(
    agent,
    initial_guess,
    estimate_method="min",
    emp_moments=None,
    moments_cov=None,
    minimize_options=None,
    criterion_kwargs=None,
    save_dir=None,
):
    fmt_init_guess = ", ".join(f"{k} = {v:.3f}" for k, v in initial_guess.items())
    multistart_text = " with multistart" if minimize_options.get("multistart") else ""
    _print_banner(
        [
            f"Estimating model using {minimize_options['algorithm']}{multistart_text} from an initial guess of",
            fmt_init_guess,
        ]
    )

    estimagic_options = _get_bounds(initial_guess)

    if estimate_method not in _ESTIMATORS:
        raise ValueError(f"Invalid estimate_method: {estimate_method}")

    res, time_to_estimate, params_attr = _ESTIMATORS[estimate_method](
        agent,
        initial_guess,
        emp_moments,
        moments_cov,
        minimize_options,
        criterion_kwargs,
        estimagic_options,
    )
    model_estimate = getattr(res, params_attr)

    minutes, seconds = divmod(time_to_estimate, 60)
    estimates = ", ".join(f"{k} = {v:.3f}" for k, v in model_estimate.items())
    _print_banner(
        [
            f"Estimated model: {agent.name}",
            f"Time to estimate: {int(minutes)} min, {int(seconds)} sec.",
            f"Estimated values: {estimates}",
        ]
    )

    # Save estimate results
    estimate_results_file = save_dir / (agent.name + "_estimate_results.csv")
    with open(estimate_results_file, "w") as f:
        writer = csv.writer(f)
        for key in model_estimate:
            writer.writerow([key, model_estimate[key]])
        writer.writerow(["time_to_estimate", time_to_estimate])
        for key, value in vars(res).items():
            writer.writerow([key, value])

    return model_estimate, res, time_to_estimate


def do_compute_se_boostrap(
    agent,
    model_estimate,
    time_to_estimate,
    bootstrap_size=50,
    seed=0,
    save_dir=None,
):
    # TODO: WRITE DOCSTRING

    # Estimate the model:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(
        f"Computing standard errors using {bootstrap_size} bootstrap replications.",
    )
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    t_bootstrap_guess = time_to_estimate * bootstrap_size
    minutes, seconds = divmod(t_bootstrap_guess, 60)
    print(f"This will take approximately {int(minutes)} min, {int(seconds)} sec.")

    t_start_bootstrap = time()
    std_errors = calculate_se_bootstrap(
        agent,
        model_estimate,
        n_draws=bootstrap_size,
        seed=seed,
        verbose=True,
    )
    t_end_bootstrap = time()
    time_to_bootstrap = t_end_bootstrap - t_start_bootstrap

    # Calculate minutes and remaining seconds
    minutes, seconds = divmod(time_to_bootstrap, 60)
    print(f"Time to bootstrap: {int(minutes)} min, {int(seconds)} sec.")

    print(f"Standard errors: DiscFac--> {std_errors[0]}, CRRA--> {std_errors[1]}")

    # Create the simple bootstrap table
    bootstrap_results_file = save_dir / (agent.name + "_bootstrap_results.csv")

    with open(bootstrap_results_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "DiscFac",
                "DiscFac_standard_error",
                "CRRA",
                "CRRA_standard_error",
            ],
        )
        writer.writerow(
            [model_estimate[0], std_errors[0], model_estimate[1], std_errors[1]],
        )

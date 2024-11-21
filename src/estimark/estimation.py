"""Demonstrates an example estimation of microeconomic dynamic stochastic optimization
problem, as described in Section 9 of Chris Carroll's Life-Cycle-Prime-Time.pdf notes.
The estimation attempts to match the age-conditional wealth profile of simulated
consumers to the median wealth holdings of seven age groups in the 2004 SCF by
varying only two parameters: the coefficient of relative risk aversion and a scaling
factor for an age-varying sequence of discount factors.  The estimation uses a
consumption-saving model with idiosyncratic shocks to permanent and transitory
income as defined in ConsIndShockModel.
"""

from __future__ import annotations

import csv
from pathlib import Path
from time import time

import estimagic as em
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Estimation methods
from estimagic.inference import get_bootstrap_samples
from scipy.optimize import approx_fprime
from statsmodels.stats.weightstats import DescrStatsW

# Import modules from core HARK libraries:
# The consumption-saving micro model
from estimark.agents import (
    BequestWarmGlowLifeCycleConsumerType,
    BequestWarmGlowLifeCyclePortfolioType,
    IndShkLifeCycleConsumerType,
    PortfolioLifeCycleConsumerType,
    WealthPortfolioLifeCycleConsumerType,
)

# Parameters for the consumer type and the estimation
from estimark.parameters import (
    age_mapping,
    bootstrap_options,
    init_calibration,
    init_params_options,
    init_subjective_labor,
    init_subjective_stock,
    minimize_options,
    sim_mapping,
)

# SCF 2004 data on household wealth
from estimark.scf import scf_data
from estimark.snp import snp_data

# =====================================================
# Define objects and functions used for the estimation
# =====================================================

agent_types = {
    "IndShock": IndShkLifeCycleConsumerType,
    "Portfolio": PortfolioLifeCycleConsumerType,
    "WarmGlow": BequestWarmGlowLifeCycleConsumerType,
    "WarmGlowPortfolio": BequestWarmGlowLifeCyclePortfolioType,
    "WealthPortfolio": WealthPortfolioLifeCycleConsumerType,
}


def make_agent(agent_name):
    for key, value in agent_types.items():
        if key in agent_name:
            agent_type = value

    calibration = init_calibration.copy()

    if "Sub" in agent_name:
        if "(Stock)" in agent_name:
            calibration.update(init_subjective_stock)
        if "(Labor)" in agent_name:
            calibration.update(init_subjective_labor)

    # Make a lifecycle consumer to be used for estimation, including simulated
    # shocks (plus an initial distribution of wealth)
    # Make a TempConsumerType for estimation
    agent = agent_type(**calibration)
    # Set the number of periods to simulate
    agent.T_sim = agent.T_cycle + 1
    # Choose to track bank balances as wealth
    track_vars = ["bNrm"]
    if "Portfolio" in agent_name:
        track_vars += ["Share"]
    agent.track_vars = track_vars

    agent.name = agent_name

    return agent


def weighted_median(values, weights):
    stats = DescrStatsW(values, weights=weights)
    return stats.quantile(0.5, return_pandas=False)


def winsored_mean(values, weights, limits):
    stats = DescrStatsW(values, weights=weights)
    qs = stats.quantile(limits, return_pandas=False)

    # discard values outside qs
    mask = (values >= qs[0]) & (values <= qs[1])
    return np.average(values[mask], weights=weights[mask])


def get_weighted_moments(
    data,
    variable=None,
    weights=None,
    groups=None,
    mapping=None,
):
    # Common variables that don't depend on whether weights are None or not
    data_variable = data[variable]
    data_groups = data[groups]
    data_weights = data[weights] if weights else None

    emp_moments = {}
    for key in mapping:
        group_data = data_variable[data_groups == key]
        group_weights = data_weights[data_groups == key] if weights else None

        # Check if the group has any data
        if not group_data.empty:
            if weights is None:
                emp_moments[key] = group_data.median()
            else:
                emp_moments[key] = weighted_median(
                    group_data.to_numpy(),
                    group_weights.to_numpy(),
                )
        # else:
        #     print(f"Warning: Group {key} does not have any data.")

    return emp_moments


def get_moments_cov(agent_name, emp_moments):
    moments_cov = em.get_moments_cov(
        scf_data,
        get_weighted_moments,
        moment_kwargs={
            "variable": "wealth_income_ratio",
            "weights": "weight",
            "groups": "age_group",
            "mapping": age_mapping,
        },
    )

    if "Port" in agent_name:
        for key1 in emp_moments:
            # Check if key1 exists in moments_cov dictionary
            if key1 not in moments_cov:
                # If it doesn't exist, create a new dictionary for this key
                moments_cov[key1] = {}

            for key2 in emp_moments:
                # Check if key2 exists in the nested dictionary under key1
                if key2 not in moments_cov[key1]:
                    # If it doesn't exist, we need to add it
                    if key1 == key2:
                        # If key1 is equal to key2, set the value to 1.0
                        moments_cov[key1][key2] = 1.0
                    else:
                        # Otherwise, set the value to 0.0
                        moments_cov[key1][key2] = 0.0

    return moments_cov


def get_empirical_moments(agent_name):
    emp_moments = get_weighted_moments(
        data=scf_data,
        variable="wealth_income_ratio",
        weights="weight",
        groups="age_group",
        mapping=age_mapping,
    )

    # Add share moments if agent is a portfolio type

    if "Portfolio" in agent_name:
        share_moments = get_weighted_moments(
            data=snp_data,
            variable="share",
            groups="age_group",
            mapping=age_mapping,
        )

        suffix = "_port"
        for key, value in share_moments.items():
            emp_moments[key + suffix] = value

    return emp_moments


def get_initial_guess(agent, params_to_estimate, save_dir):
    agent_name = agent.name

    agent_params = []
    for key in params_to_estimate:
        if hasattr(agent, key):
            agent_params.append(key)
        else:
            print(f"Agent {agent_name} does not have parameter: {key}")

    # start from previous estimation results if available
    csv_file_path = save_dir / (agent_name + "_estimate_results.csv")

    try:
        res = pd.read_csv(csv_file_path, header=None)
        temp_dict = res.set_index(res.columns[0])[res.columns[1]].to_dict()
    except (FileNotFoundError, IndexError):
        temp_dict = init_params_options.get("init_guess", {})

    initial_guess = {
        key: float(temp_dict.get(key, init_params_options["init_guess"][key]))
        for key in agent_params
    }

    return initial_guess


# Define the objective function for the simulated method of moments estimation
def simulate_moments(params, agent=None, emp_moments=None):
    """A quick check to make sure that the parameter values are within bounds.
    Far flung falues of DiscFac or CRRA might cause an error during solution or
    simulation, so the objective function doesn't even bother with them.
    """
    # Update the agent with a new path of DiscFac based on this DiscFac (and a new CRRA)

    agent.assign_parameters(**params)

    if hasattr(agent, "BeqCRRA"):
        agent.BeqCRRA = agent.CRRA

    # ensure subjective beliefs are used for solution
    if "(Stock)" in agent.name and "Portfolio" in agent.name:
        agent.RiskyAvg = init_subjective_stock["RiskyAvg"]
        agent.RiskyStd = init_subjective_stock["RiskyStd"]
        agent.Rfree = init_subjective_stock["Rfree"]
        agent.update_RiskyDstn()
    if "(Labor)" in agent.name:
        agent.TranShkStd = init_subjective_labor["TranShkStd"]
        agent.PermShkStd = init_subjective_labor["PermShkStd"]
        agent.update_income_process()

    agent.update()

    # Solve the model for these parameters, then simulate wealth data
    agent.solve()  # Solve the microeconomic model

    # simulate with true parameters (override subjective beliefs)
    if "(Stock)" in agent.name and "Portfolio" in agent.name:
        agent.RiskyAvg = init_subjective_stock["RiskyAvgTrue"]
        agent.RiskyStd = init_subjective_stock["RiskyStdTrue"]
        agent.Rfree = init_subjective_stock["Rfree"]
        agent.update_RiskyDstn()
    # for labor keep same process as subjective beliefs
    if "(Labor)" in agent.name:
        agent.TranShkStd = init_subjective_labor["TranShkStd"]
        agent.PermShkStd = init_subjective_labor["PermShkStd"]
        agent.update_income_process()

    agent.update()

    max_sim_age = agent.T_cycle + 1
    # Initialize the simulation by clearing histories, resetting initial values
    agent.initialize_sim()
    # agent.make_shock_history()
    agent.simulate(max_sim_age)  # Simulate histories of consumption and wealth
    # Take "wealth" to mean bank balances before receiving labor income
    sim_w_history = agent.history["bNrm"]

    # Find the distance between empirical data and simulated medians for each age group

    sim_moments = {
        key: np.median(sim_w_history[cohort_idx])
        for key, cohort_idx in sim_mapping.items()
        if key in emp_moments
    }

    if "Portfolio" in agent.name:
        sim_share_history = agent.history["Share"]
        share_moments = {}
        for key, cohort_idx in sim_mapping.items():
            key_port = key + "_port"
            if key_port in emp_moments:
                share_moments[key_port] = np.median(sim_share_history[cohort_idx])
        sim_moments.update(share_moments)

    return sim_moments


def calculate_weights(emp_moments):
    n_port_stats = sum(1 for k in emp_moments if "_port" in k)
    max_w_stat = max(emp_moments.values())

    port_fac = (
        (len(emp_moments) - n_port_stats) / n_port_stats if n_port_stats != 0 else 1.0
    )

    port_fac = 1.0

    # Using dictionary comprehension to create weights
    weights = {
        k: (1 / max_w_stat if "_port" not in k else port_fac)
        for k, v in emp_moments.items()
    }

    return weights


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
    DiscFac : float
        An adjustment factor to a given age-varying sequence of discount factors.
        I.e. DiscFac[t] = DiscFac*timevary_DiscFac[t].
    CRRA : float
        Coefficient of relative risk aversion.
    agent : ConsumerType
        The consumer type to be used in the estimation, with all necessary para-
        meters defined except the discount factor and CRRA.
    bounds_DiscFac : (float,float)
        Lower and upper bounds on DiscFac; if outside these bounds, the function
        simply returns a "penalty value".
    bounds_DiscFac : (float,float)
        Lower and upper bounds on CRRA; if outside these bounds, the function
        simply returns a "penalty value".
    empirical_data : np.array
        Array of wealth-to-permanent-income ratios in the data.
    empirical_weights : np.array
        Weights for each observation in empirical_data.
    empirical_groups : np.array
        Array of integers listing the age group for each observation in empirical_data.
    mapping : [np.array]
        List of arrays of "simulation ages" for each age grouping.  E.g. if the
        0th element is [1,2,3,4,5], then these time indices from the simulation
        correspond to the 0th empirical age group.

    Returns
    -------
    distance_sum : float
        Sum of distances between empirical data observations and the corresponding
        median wealth-to-permanent-income ratio in the simulation.

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


# Define the bootstrap procedure
def calculate_se_bootstrap(
    agent,
    initial_estimate,
    n_draws=50,
    seed=0,
    verbose=False,
):
    """Calculates standard errors by repeatedly re-estimating the model with datasets
    resampled from the actual data.

    Parameters
    ----------
    initial_estimate : [float,float]
        The estimated [DiscFac,CRRA], for use as an initial guess for each
        re-estimation in the bootstrap procedure.
    N : int
        Number of times to resample data and re-estimate the model.
    seed : int
        Seed for the random number generator.
    verbose : boolean
        Indicator for whether extra output should be printed for the user.

    Returns
    -------
    standard_errors : [float,float]
        Standard errors calculated by bootstrap: [DiscFac_std_error, CRRA_std_error].

    """
    t_0 = time()

    # Generate a list of seeds for generating bootstrap samples
    RNG = np.random.default_rng(seed)
    seed_list = RNG.integers(2**31 - 1, size=n_draws)

    # Estimate the model N times, recording each set of estimated parameters
    estimate_list = []
    for n in range(n_draws):
        t_start = time()

        # Bootstrap a new dataset by resampling from the original data
        bootstrap_data = get_bootstrap_samples(data=scf_data, rng=RNG)

        # Find moments with bootstrapped sample
        bootstrap_moments = get_weighted_moments(
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

        # Report progress of the bootstrap
    if verbose:
        print(
            f"Finished bootstrap estimation #{n + 1} of {n_draws} in {t_now - t_start} seconds ({t_now - t_0} cumulative)",
        )

    # Calculate the standard errors for each parameter
    estimate_array = (np.array(estimate_list)).T
    DiscFac_std_error = np.std(estimate_array[0])
    CRRA_std_error = np.std(estimate_array[1])

    return [DiscFac_std_error, CRRA_std_error]


# =================================================================
# Done defining objects and functions.  Now run them (if desired).
# =================================================================


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
    fmt_init_guess = [f"{key} = {value:.3f}" for key, value in initial_guess.items()]
    multistart_text = " with multistart" if minimize_options.get("multistart") else ""
    statement1 = f"Estimating model using {minimize_options['algorithm']}{multistart_text} from an initial guess of"
    statement2 = ", ".join(fmt_init_guess)
    max_len = max(len(statement1), len(statement2))
    dash_line = "-" * max_len

    # Use f-string for padding
    statement1 = f"{statement1:^{max_len}}"
    statement2 = f"{statement2:^{max_len}}"

    print(dash_line)
    print(statement1)
    print(statement2)
    print(dash_line)

    upper_bounds = {
        key: value
        for key, value in init_params_options["upper_bounds"].items()
        if key in initial_guess
    }

    lower_bounds = {
        key: value
        for key, value in init_params_options["lower_bounds"].items()
        if key in initial_guess
    }

    estimagic_options = {"upper_bounds": upper_bounds, "lower_bounds": lower_bounds}

    if estimate_method == "min":
        res, time_to_estimate = estimate_min(
            agent,
            msm_criterion,
            initial_guess,
            emp_moments,
            minimize_options,
            criterion_kwargs=criterion_kwargs,
            estimagic_options=estimagic_options,
        )

        model_estimate = res.params

    elif estimate_method == "msm":
        res, time_to_estimate = estimate_msm(
            agent,
            simulate_moments,
            emp_moments,
            moments_cov,
            initial_guess,
            minimize_options,
            estimagic_options=estimagic_options,
        )

        model_estimate = res._params

    else:
        raise ValueError(f"Invalid estimate_method: {estimate_method}")

    # Calculate minutes and remaining seconds
    minutes, seconds = divmod(time_to_estimate, 60)
    statement1 = f"Estimated model: {agent.name}"
    statement2 = f"Time to estimate: {int(minutes)} min, {int(seconds)} sec."
    estimates = [f"{key} = {value:.3f}" for key, value in model_estimate.items()]
    statement3 = "Estimated values: " + ", ".join(estimates)
    dash_len = max(len(statement1), len(statement2), len(statement3))
    print(statement1)
    print(statement2)
    print(statement3)
    print("-" * dash_len)

    # Create the simple estimate table
    estimate_results_file = save_dir / (agent.name + "_estimate_results.csv")

    keys_to_save = vars(res)

    with open(estimate_results_file, "w") as f:
        writer = csv.writer(f)

        for key in model_estimate:
            writer.writerow([key, model_estimate[key]])

        writer.writerow(["time_to_estimate", time_to_estimate])

        if keys_to_save is not None:
            for key in keys_to_save:
                writer.writerow([key, getattr(res, key)])

    return model_estimate, res, time_to_estimate


def do_compute_se_boostrap(
    agent,
    model_estimate,
    time_to_estimate,
    bootstrap_size=50,
    seed=0,
    save_dir=None,
):
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
    bootstrap_results_file = save_dir + agent.name + "_bootstrap_results.csv"

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


def do_compute_sensitivity(agent, model_estimate, emp_moments, save_dir=None):
    print("``````````````````````````````````````````````````````````````````````")
    print("Computing sensitivity measure.")
    print("``````````````````````````````````````````````````````````````````````")

    # Find the Jacobian of the function that simulates moments

    n_moments = len(emp_moments)
    jac = np.array(
        [
            approx_fprime(
                model_estimate,
                lambda params: simulate_moments(params, agent=agent)[j],
                epsilon=0.01,
            )
            for j in range(n_moments)
        ],
    )

    # Compute sensitivity measure. (all moments weighted equally)
    sensitivity = np.dot(np.linalg.inv(np.dot(jac.T, jac)), jac.T)

    # Create lables for moments in the plots
    moment_labels = emp_moments.keys()

    # Plot
    fig, axs = plt.subplots(len(model_estimate))
    fig.set_tight_layout(True)

    axs[0].bar(range(n_moments), sensitivity[0, :], tick_label=moment_labels)
    axs[0].set_title("DiscFac")
    axs[0].set_ylabel("Sensitivity")
    axs[0].set_xlabel("Median W/Y Ratio")

    axs[1].bar(range(n_moments), sensitivity[1, :], tick_label=moment_labels)
    axs[1].set_title("CRRA")
    axs[1].set_ylabel("Sensitivity")
    axs[1].set_xlabel("Median W/Y Ratio")

    plt.savefig(save_dir + agent.name + "Sensitivity.pdf")
    plt.savefig(save_dir + agent.name + "Sensitivity.png")
    plt.savefig(save_dir + agent.name + "Sensitivity.svg")

    plt.show()


def do_make_contour_plot(agent, model_estimate, emp_moments, save_dir=None):
    print("``````````````````````````````````````````````````````````````````````")
    print("Creating the contour plot.")
    print("``````````````````````````````````````````````````````````````````````")
    t_start_contour = time()
    DiscFac_star, CRRA_star = model_estimate
    grid_density = 20  # Number of parameter values in each dimension
    level_count = 100  # Number of contour levels to plot
    DiscFac_list = np.linspace(
        max(DiscFac_star - 0.25, 0.5),
        min(DiscFac_star + 0.25, 1.05),
        grid_density,
    )
    CRRA_list = np.linspace(max(CRRA_star - 5, 2), min(CRRA_star + 5, 8), grid_density)
    CRRA_mesh, DiscFac_mesh = np.meshgrid(CRRA_list, DiscFac_list)
    smm_obj_levels = np.empty([grid_density, grid_density])
    for j in range(grid_density):
        DiscFac = DiscFac_list[j]
        for k in range(grid_density):
            CRRA = CRRA_list[k]
            smm_obj_levels[j, k] = msm_criterion(
                np.array([DiscFac, CRRA]),
                agent=agent,
                emp_moments=emp_moments,
            )
    smm_contour = plt.contourf(CRRA_mesh, DiscFac_mesh, smm_obj_levels, level_count)
    t_end_contour = time()
    time_to_contour = t_end_contour - t_start_contour

    # Calculate minutes and remaining seconds
    minutes, seconds = divmod(time_to_contour, 60)
    print(f"Time to contour: {int(minutes)} min, {int(seconds)} sec.")

    plt.colorbar(smm_contour)
    plt.plot(model_estimate[1], model_estimate[0], "*r", ms=15)
    plt.xlabel(r"coefficient of relative risk aversion $\rho$", fontsize=14)
    plt.ylabel(r"discount factor adjustment $\beth$", fontsize=14)
    plt.savefig(save_dir + agent.name + "SMMcontour.pdf")
    plt.savefig(save_dir + agent.name + "SMMcontour.png")
    plt.savefig(save_dir + agent.name + "SMMcontour.svg")
    plt.show()


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


def estimate(
    agent_name,
    params_to_estimate,
    estimate_model=True,
    estimate_method="min",
    compute_se_bootstrap=False,
    compute_sensitivity=False,
    make_contour_plot=False,
    save_dir=None,
    emp_moments=None,
    moments_cov=None,
):
    """Run the main estimation procedure for Life-Cycle-Prime-Time.

    Parameters
    ----------
    estimate_model : bool
        Whether to estimate the model using Nelder-Mead. When True, this is a low-time, low-memory operation.

    compute_standard_errors : bool
        Whether to compute standard errors on the estiamtion of the model.

    make_contour_plot : bool
        Whether to make the contour plot associate with the estiamte.

    Returns
    -------
    None

    """
    save_dir = Path(save_dir).resolve() if save_dir is not None else Path.cwd()
    save_dir.mkdir(parents=True, exist_ok=True)

    ############################################################
    # Make agent
    ############################################################

    agent = make_agent(agent_name)

    ############################################################
    # Get initial guess
    ############################################################

    initial_guess = get_initial_guess(agent, params_to_estimate, save_dir)

    ############################################################
    # Get empirical moments
    ############################################################

    if emp_moments is None:
        emp_moments = get_empirical_moments(agent_name)

        print("Calculated empirical moments.")

    weights = calculate_weights(emp_moments)

    ############################################################
    # Get moments covariance matrix
    ############################################################

    if moments_cov is None and estimate_method == "msm":
        moments_cov = get_moments_cov(agent_name, emp_moments)

        print("Calculated moments covariance matrix.")

    ############################################################
    # Estimate model
    ############################################################

    if estimate_model:
        model_estimate, res, time_to_estimate = do_estimate_model(
            agent,
            initial_guess,
            estimate_method=estimate_method,
            emp_moments=emp_moments,
            moments_cov=moments_cov,
            minimize_options=minimize_options,
            criterion_kwargs={"weights": weights},
            save_dir=save_dir,
        )

    # Compute standard errors by bootstrap
    if compute_se_bootstrap:
        do_compute_se_boostrap(
            agent,
            model_estimate,
            time_to_estimate,
            save_dir=save_dir,
            **bootstrap_options,
        )

    # Compute sensitivity measure
    if compute_sensitivity:
        do_compute_sensitivity(
            agent,
            model_estimate,
            initial_guess,
            save_dir=save_dir,
        )

    # Make a contour plot of the objective function
    if make_contour_plot:
        do_make_contour_plot(
            agent,
            model_estimate,
            emp_moments,
            save_dir=save_dir,
        )


if __name__ == "__main__":
    # Set booleans to determine which tasks should be done
    # Which agent type to estimate ("IndShock" or "Portfolio")
    local_agent_name = "WealthPortfolio"
    local_params_to_estimate = ["CRRA", "WealthShare", "WealthShift"]
    local_estimate_model = True  # Whether to estimate the model
    # Whether to get standard errors via bootstrap
    local_compute_se_bootstrap = False
    # Whether to compute a measure of estimates' sensitivity to moments
    local_compute_sensitivity = False
    # Whether to make a contour map of the objective function
    local_make_contour_plot = False
    local_save_dir = "content/tables/min"

    estimate(
        agent_name=local_agent_name,
        params_to_estimate=local_params_to_estimate,
        estimate_model=local_estimate_model,
        compute_se_bootstrap=local_compute_se_bootstrap,
        compute_sensitivity=local_compute_sensitivity,
        make_contour_plot=local_make_contour_plot,
        save_dir=local_save_dir,
    )

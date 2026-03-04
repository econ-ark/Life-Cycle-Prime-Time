"""Core orchestration: agent construction, initial guesses, and main estimate loop."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from estimark.agents import (
    BequestWarmGlowLifeCycleConsumerType,
    BequestWarmGlowLifeCyclePortfolioType,
    IndShkLifeCycleConsumerType,
    PortfolioLifeCycleConsumerType,
    WealthPortfolioLifeCycleConsumerType,
)
from estimark.parameters import (
    bootstrap_options,
    init_calibration,
    init_params_options,
    init_subjective_labor,
    init_subjective_stock,
    minimize_options,
)

from .moments import calculate_weights, get_empirical_moments, get_moments_cov
from .optimization import do_compute_se_boostrap, do_estimate_model
from .simulation import simulate_moments
from .visualization import do_compute_sensitivity, do_make_contour_plot

agent_types = {
    "IndShock": IndShkLifeCycleConsumerType,
    "Portfolio": PortfolioLifeCycleConsumerType,
    "WarmGlow": BequestWarmGlowLifeCycleConsumerType,
    "WarmGlowPortfolio": BequestWarmGlowLifeCyclePortfolioType,
    "WealthPortfolio": WealthPortfolioLifeCycleConsumerType,
}


def make_agent(agent_name):
    """
    Construct an instance of an AgentType subclass that can be used in the structural
    estimation. The specific class used, as well as some of the exogenously calibrated
    parameters, depend on whether certain strings appear in the input to the function:

    NAME --> AgentType subclass
    "IndShock" --> IndShkLifeCycleConsumerType
    "Portfolio" --> PortfolioLifeCycleConsumerType
    "WarmGlow" --> BequestWarmGlowLifeCycleConsumerType
    "WarmGlowPortfolio" --> BequestWarmGlowLifeCyclePortfolioType
    "WealthPortfolio" --> WealthPortfolioLifeCycleConsumerType

    If (Stock) appears in agent_name, then the agent will solve its problem using
    parameters estimated from subjective beliefs about stock return (but simulate
    using values from empirical observations).

    If (Labor) appears in agent_name, then the agent will solve its problem using
    parameters estimated from subjective beliefs about labor income risk (but sim-
    ulate using values from empirical observations).

    Parameters
    ----------
    agent_name : str
        Name of the agent specification, which determines details of its type
        and exogenous parameters.

    Returns
    -------
    agent : AgentType
        Instance of some AgentType subclass, which can be used in the estimation.
        It will have default parameters until set otherwise.
    """
    agent_type = None
    for key, value in agent_types.items():
        if key in agent_name:
            agent_type = value
    if agent_type is None:
        raise ValueError(f"No agent type found for name: {agent_name!r}")

    calibration = init_calibration.copy()

    if "Sub" in agent_name:
        if "(Stock)" in agent_name:
            calibration.update(init_subjective_stock)
        if "(Labor)" in agent_name:
            calibration.update(init_subjective_labor)

    # Make a lifecycle consumer to be used for estimation
    agent = agent_type(**calibration)
    agent.name = agent_name

    # Choose to track bank balances as wealth, and track risky asset share if needed
    track_vars = ["bNrm"]
    if "Portfolio" in agent_name:
        track_vars += ["Share"]
    agent.track_vars = track_vars

    return agent


def get_initial_guess(agent, params_to_estimate, save_dir):
    """
    Generate an initial guess of the parameters to be estimated by looking for
    prior estimates of the same specification, or defaulting to values specified
    in the parameters file.

    Parameters
    ----------
    agent : AgentType
        Instance of some AgentType subclass that will be used in the estimation.
        Used to verify that the parameters to be estimated actually exist.
    params_to_estimate : [str]
        List of strings naming variables to be estimated.
    save_dir : str
        Directory where estimation output will be stored, and maybe has already
        been stored. Used to check whether this specification has already been run.

    Returns
    -------
    initial_guess : dict
        Mapping from parameter names to initial guess values.
    """
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
    NEED TO MAKE CORRECT INPUTS

    Returns
    -------
    None
    """
    save_dir = Path(save_dir).resolve() if save_dir is not None else Path.cwd()
    save_dir.mkdir(parents=True, exist_ok=True)

    agent = make_agent(agent_name)
    initial_guess = get_initial_guess(agent, params_to_estimate, save_dir)

    if emp_moments is None:
        emp_moments, weight_sum = get_empirical_moments(agent_name)
        print("Calculated empirical moments.")
    else:
        _, weight_sum = get_empirical_moments(agent_name)

    weights = calculate_weights(emp_moments, weight_sum)

    if moments_cov is None and estimate_method == "msm":
        moments_cov = get_moments_cov(agent_name, emp_moments)
        print("Calculated moments covariance matrix.")

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


def prepare_model(agent_name, params_to_estimate):
    """
    Generate objects that can be used to estimate and explore the requested model.

    Parameters
    ----------
    agent_name : str
        Name of the specification that will be run, which is used to determine
        which subclass of agents to use.
    params_to_estimate : [str]
        List of parameter names that will be used in the estimation.

    Returns
    -------
    estimation_agents : AgentType
        Instance of some AgentType subclass that will be used in the estimation.
    empirical_moments : dict
        Dictionary of keys naming moments and their empirical values.
    moment_weights : dict
        Dictionary of keys naming moments and their weights.
    objective_function : Callable
        Function that takes a single array of parameter values as an argument,
        ordered as the names in params_to_estimate, and returns the value of the
        MSM criterion at those parameters.
    sim_moment_function: Callable
        Function that takes a single array of parameter values as an argument,
        ordered as the names in params_to_estimate, and returns a dictionary of
        simulated moments at those parameters.
    plot_moment_function: Callable
        Function that takes a single array of parameter values as an argument,
        ordered as the names in params_to_estimate, and makes two plots of the
        simulated vs empirical moment fit.
    """
    # Make basic objects using previously defined functions
    estimation_agents = make_agent(agent_name)
    empirical_moments, weight_sum = get_empirical_moments(agent_name)
    moment_weights = calculate_weights(empirical_moments, weight_sum)

    # Make a local function that can return the objective function value or the
    # dictionary of simulated moments, or plot the moment fit
    def temp_func(param_vec, return_moments=False, plot_moments=False):
        params = {
            params_to_estimate[j]: param_vec[j] for j in range(len(params_to_estimate))
        }
        emp_moments = empirical_moments.copy()
        sim_moments = simulate_moments(params, estimation_agents, emp_moments)

        if plot_moments:
            wealth_keys = [key for key in sim_moments if "_port" not in key]
            port_keys = [key for key in sim_moments if "_port" in key]
            wealth_emp = np.array([emp_moments[k] for k in wealth_keys])
            wealth_sim = np.array([sim_moments[k] for k in wealth_keys])
            port_emp = np.array([emp_moments[k] for k in port_keys])
            port_sim = np.array([sim_moments[k] for k in port_keys])
            wealth_labels = [x[1:3] for x in wealth_keys]
            port_labels = [x[1:3] for x in port_keys]

            plt.plot(wealth_emp, ".k", ms=10)
            plt.plot(wealth_sim, "-b")
            plt.xticks(np.arange(wealth_emp.size), labels=wealth_labels)
            plt.xlabel("Age group")
            plt.ylabel("Wealth/income ratio")
            plt.tight_layout()
            plt.ylim(0.0, 14.0)
            plt.show()

            plt.plot(port_emp, ".k", ms=10)
            plt.plot(port_sim, "-r")
            plt.xticks(np.arange(port_emp.size), labels=port_labels)
            plt.xlabel("Age group")
            plt.ylabel("Risky asset share")
            plt.ylim(0.0, 1.0)
            plt.tight_layout()
            plt.show()

            return None

        if return_moments:
            return sim_moments

        errors = np.array(
            [
                float(moment_weights[key] * (sim_moments[key] - empirical_moments[key]))
                for key in empirical_moments
            ],
        )
        sse = np.sum(errors**2)
        return sse

    # Make two versions of that temporary function: one for the objective function
    # and the other that just produces moments
    objective_function = lambda x: temp_func(x, False, False)
    sim_moment_function = lambda x: temp_func(x, True, False)
    plot_moment_function = lambda x: temp_func(x, False, True)

    # Return all of the useful things
    return (
        estimation_agents,
        empirical_moments,
        moment_weights,
        objective_function,
        sim_moment_function,
        plot_moment_function,
    )

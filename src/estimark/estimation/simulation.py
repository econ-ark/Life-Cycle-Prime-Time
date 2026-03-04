"""Simulation: solve agents under subjective beliefs, simulate, collect moments."""

from __future__ import annotations

import numpy as np

from estimark.parameters import (
    init_subjective_labor,
    init_subjective_stock,
    sim_mapping,
    true_stock_params,
)


def _apply_subjective_beliefs(agent):
    """Configure subjective beliefs for solving the agent's problem."""
    if "(Stock)" in agent.name and "Portfolio" in agent.name:
        agent.assign_parameters(**init_subjective_stock)
        agent.construct("RiskyDstn", "ShockDstn")
    if "(Labor)" in agent.name:
        agent.assign_parameters(**init_subjective_labor)
        agent.update_income_process()


def _apply_true_beliefs(agent):
    """Override subjective beliefs with true parameters for simulation."""
    if "(Stock)" in agent.name and "Portfolio" in agent.name:
        agent.assign_parameters(**true_stock_params)
        agent.construct("RiskyDstn", "ShockDstn")
    if "(Labor)" in agent.name:
        agent.TranShkStd = init_subjective_labor["TranShkStd"]
        agent.PermShkStd = init_subjective_labor["PermShkStd"]
        agent.update_income_process()


def _collect_sim_moments(agent, emp_moments):
    """Extract simulated median moments from agent history."""
    sim_w_history = agent.history["bNrm"]
    sim_moments = {
        key: np.median(sim_w_history[cohort_idx])
        for key, cohort_idx in sim_mapping.items()
        if key in emp_moments
    }

    if "Portfolio" in agent.name:
        sim_share_history = agent.history["Share"]
        sim_moments.update(
            {
                key + "_port": np.median(sim_share_history[cohort_idx])
                for key, cohort_idx in sim_mapping.items()
                if key + "_port" in emp_moments
            }
        )

    return sim_moments


def simulate_moments(params, agent, emp_moments):
    """
    Generate simulated moments by solving and simulating the agents at the given
    parameters. Returns a dictionary that corresponds to the empirical moments.

    Parameters
    ----------
    params : dict
        Mapping from parameters to be estimated to parameter values.
    agent : AgentType
        Instance of some AgentType subclass, representing the model to be solved
        and simulated to generate moments.
    emp_moments : dict
        Mapping from moment names to empirical moments.

    Returns
    -------
    sim_moments : dict
        Dictionary that maps from moment names to simulated moments.
    """
    # Update the agent with new parameters
    agent.assign_parameters(**params)
    if hasattr(agent, "BeqCRRA"):
        agent.BeqCRRA = agent.CRRA

    _apply_subjective_beliefs(agent)

    agent.update()
    if "WarmGlow" in agent.name:
        agent.BeqFac = agent.BeqMPC ** (-agent.CRRA)
        agent.BeqShift = agent.BeqInt / agent.BeqMPC

    agent.solve()

    _apply_true_beliefs(agent)
    agent.update()

    agent.initialize_sim()
    agent.simulate(agent.T_cycle + 1)

    return _collect_sim_moments(agent, emp_moments)

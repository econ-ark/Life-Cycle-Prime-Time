"""Empirical moment computation: weighted medians, covariance, and weights."""

from __future__ import annotations

import estimagic as em
import numpy as np
from statsmodels.stats.weightstats import DescrStatsW

from estimark.parameters import age_mapping
from estimark.scf import scf_data
from estimark.snp import snp_data


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
    variable,
    weights=None,
    groups=None,
    mapping=None,
):
    """
    Make a dictionary that maps from moment names to moments used in the SMM
    objective function, generating medians of some variable conditional on
    being within particular values for some data grouping.

    Parameters
    ----------
    data : dict ?
        The dataset from which the moments are being extracted, with variable
        names as keys and an array of data as values.
    variable : str
        Name of the variable for which conditional medians will be calculated.
    weights : str or None
        Name of the weighting variable in the dataset, if any.
    groups : str or None
        Name of the variable to condition the medians on.
    mapping : iterable or None
        List or dictionary of values that the variable named in groups can have.

    Returns
    -------
    emp_moments : dict
        Dictionary mapping from keys of mapping input to conditional medians.
    weight_sum : dict
        Dictionary mapping from keys of mapping input to total weight of group.
    """
    # Common variables that don't depend on whether weights are None or not
    data_variable = data[variable]
    data_groups = data[groups]
    data_weights = data[weights] if weights else None

    emp_moments = {}
    weight_sum = {}
    for key in mapping:
        group_data = data_variable[data_groups == key]
        group_weights = data_weights[data_groups == key] if weights else None
        W = np.sum(group_weights)
        weight_sum[key] = W

        # Check if the group has any data
        if not group_data.empty:
            if weights is None:
                emp_moments[key] = group_data.median()
            else:
                emp_moments[key] = weighted_median(
                    group_data.to_numpy(),
                    group_weights.to_numpy(),
                )

    return emp_moments, weight_sum


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
        # Fill in identity-diagonal entries for any moment keys missing from the
        # covariance matrix (portfolio share moments are not in SCF wealth data).
        for key1 in emp_moments:
            moments_cov.setdefault(key1, {})
            for key2 in emp_moments:
                moments_cov[key1].setdefault(key2, 1.0 if key1 == key2 else 0.0)

    return moments_cov


def get_empirical_moments(agent_name):
    """
    Construct a dictionary of empirical moments for this specification. This
    always includes age-conditional median wealth values, and also includes
    risky portfolio shares if the specification name includes "Portfolio".

    Parameters
    ----------
    agent_name : str
        Name of the current specification.

    Returns
    -------
    emp_moments : dict
        Dictionary with median wealth (and risky asset shares) empirical moments.
    weight_sum : dict
        Dictionary with median wealth (and risky asset shares) total empirical
        weights from the dataset.
    """
    emp_moments, weight_sum = get_weighted_moments(
        data=scf_data,
        variable="wealth_income_ratio",
        weights="weight",
        groups="age_group",
        mapping=age_mapping,
    )
    emp_moments = {key: float(emp_moments[key]) for key in emp_moments}

    # Add share moments if agent is a portfolio type
    if "Portfolio" in agent_name:
        share_moments, share_weight_sum = get_weighted_moments(
            data=snp_data,
            variable="share",
            groups="age_group",
            mapping=age_mapping,
        )

        suffix = "_port"
        for key, value in share_moments.items():
            emp_moments[key + suffix] = value
        for key, value in share_weight_sum.items():
            weight_sum[key + suffix] = value

    return emp_moments, weight_sum


def calculate_weights(emp_moments, weight_sum):
    """
    Generate a dictionary of all moment weights, loading both median wealth-to-
    income ratios and risky asset shares into a single object.

    Parameters
    ----------
    emp_moments : dict
        Mapping from moment names to empirical moments. Used to make the keys
        for the weighting dictionary.
    weight_sum: dict
        Mapping from moment names to total empirical weight from the dataset.
        This *can* be used to make weights using a different scheme.

    Returns
    -------
    weights : dict
        Mapping from moment names to weights.

    """
    n_port_stats = np.sum([1 for k in emp_moments if "_port" in k])
    n_wealth_stats = len(emp_moments) - n_port_stats
    max_w_stat = float(max(emp_moments.values()))
    W_total = np.sum([np.sqrt(weight_sum[k]) for k in weight_sum if "_port" not in k])
    W_avg = W_total / n_wealth_stats

    port_fac = np.sqrt(n_wealth_stats / n_port_stats) if n_port_stats != 0 else 1.0
    # port_fac = 1.0

    # Using dictionary comprehension to create weights
    weights = {
        k: (
            (np.sqrt(weight_sum[k]) / W_avg) ** 0.0 / max_w_stat
            if "_port" not in k
            else port_fac
        )
        for k, v in emp_moments.items()
    }

    return weights

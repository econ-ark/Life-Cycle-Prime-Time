"""Estimation package for Life-Cycle-Prime-Time."""

from __future__ import annotations

from .core import agent_types, estimate, get_initial_guess, make_agent, prepare_model
from .moments import (
    calculate_weights,
    get_empirical_moments,
    get_moments_cov,
    get_weighted_moments,
    weighted_median,
    winsored_mean,
)
from .optimization import (
    calculate_se_bootstrap,
    do_compute_se_boostrap,
    do_estimate_model,
    estimate_min,
    estimate_msm,
    msm_criterion,
)
from .simulation import simulate_moments
from .visualization import do_compute_sensitivity, do_make_contour_plot

__all__ = [
    "agent_types",
    "calculate_se_bootstrap",
    "calculate_weights",
    "do_compute_se_boostrap",
    "do_compute_sensitivity",
    "do_estimate_model",
    "do_make_contour_plot",
    "estimate",
    "estimate_min",
    "estimate_msm",
    "get_empirical_moments",
    "get_initial_guess",
    "get_moments_cov",
    "get_weighted_moments",
    "make_agent",
    "msm_criterion",
    "prepare_model",
    "simulate_moments",
    "weighted_median",
    "winsored_mean",
]

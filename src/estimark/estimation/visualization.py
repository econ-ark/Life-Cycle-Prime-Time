"""Visualization: sensitivity plots and contour maps."""

from __future__ import annotations

from time import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import approx_fprime

from .optimization import msm_criterion
from .simulation import simulate_moments


def do_compute_sensitivity(agent, model_estimate, emp_moments, save_dir=None):
    # TODO: WRITE DOCSTRING

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

    plt.savefig(save_dir / (agent.name + "Sensitivity.pdf"))
    plt.savefig(save_dir / (agent.name + "Sensitivity.png"))
    plt.savefig(save_dir / (agent.name + "Sensitivity.svg"))

    plt.show()


def do_make_contour_plot(agent, model_estimate, emp_moments, save_dir=None):
    # TODO: WRITE DOCSTRING

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
    plt.savefig(save_dir / (agent.name + "SMMcontour.pdf"))
    plt.savefig(save_dir / (agent.name + "SMMcontour.png"))
    plt.savefig(save_dir / (agent.name + "SMMcontour.svg"))
    plt.show()

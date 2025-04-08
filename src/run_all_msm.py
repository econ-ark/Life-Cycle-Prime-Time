from __future__ import annotations

import itertools

import dask
from dask.distributed import Client

from estimark.estimation import estimate, get_empirical_moments, get_moments_cov
from estimark.options import low_resource

agent_names = [
    "IndShock",
    "Portfolio",
    "WarmGlow",
    "WarmGlowPortfolio",
    "WealthPortfolio",
]


def run_replication():
    inds_emp_moments = get_empirical_moments("IndShock")
    port_emp_moments = get_empirical_moments("Porfolio")

    inds_moments_cov = get_moments_cov("IndShock", inds_emp_moments)
    port_moments_cov = get_moments_cov("Porfolio", port_emp_moments)

    client = Client(threads_per_worker=10, n_workers=20)

    lazy_results = []

    for agent_name in agent_names:
        for sub_stock, sub_labor in itertools.product(range(2), repeat=2):
            temp_agent_name = agent_name
            if sub_stock or sub_labor:
                temp_agent_name += "Sub"
                if sub_stock:
                    temp_agent_name += "(Stock)"
                if sub_labor:
                    temp_agent_name += "(Labor)"
                temp_agent_name += "Market"

            replication_specs = low_resource.copy()
            replication_specs["agent_name"] = temp_agent_name
            replication_specs["save_dir"] = "docs/tables/msm"

            print("Model: ", replication_specs["agent_name"])

            if "Portfolio" in replication_specs["agent_name"]:
                replication_specs["emp_moments"] = port_emp_moments
                replication_specs["moments_cov"] = port_moments_cov
            else:
                replication_specs["emp_moments"] = inds_emp_moments
                replication_specs["moments_cov"] = inds_moments_cov

            replication_specs["estimate_method"] = "msm"

            lazy_result = dask.delayed(estimate)(**replication_specs)
            lazy_results.append(lazy_result)

    dask.compute(*lazy_results)

    client.close()


if __name__ == "__main__":
    run_replication()

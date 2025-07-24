from __future__ import annotations

import logging

from estimark.estimation import estimate
from estimark.options import low_resource

# Configure logging to show INFO level messages
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

agent_names = [
    "Portfolio",
    "WealthPortfolio",
    "WarmGlowPortfolio",
]


# Ask the user which replication to run, and run it:
def run_replication() -> None:
    for agent_name in agent_names:
        for sub_stock in [0]:
            temp_agent_name = agent_name
            if sub_stock:
                temp_agent_name += "Sub(Stock)Market"

            replication_specs = low_resource.copy()
            replication_specs["agent_name"] = temp_agent_name
            replication_specs["save_dir"] = "docs/tables/TRP"

            logging.info("Model: %s", replication_specs["agent_name"])

            estimate(**replication_specs)

    logging.info("All replications complete.")


if __name__ == "__main__":
    run_replication()

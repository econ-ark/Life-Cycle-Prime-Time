"""Run all of the plots and tables in Life-Cycle-Prime-Time.

To execute, do the following on the Python command line:

    from HARK.[YOUR-MODULE-NAME-HERE].do_all import run_replication
    run_replication()

You will be presented with an interactive prompt that asks what level of
replication you would like to have.

More Details
------------

This example script allows the user to create all of the figures and tables
modules for Life-Cycle-Prime-Time.StructuralEstimation.

This is example is kept as simple and minimal as possible to illustrate the
format of a "replication archive."

The file structure is as follows:

./Life-Cycle-Prime-Time/
    calibration/        # Directory that contain the necessary code and data to parameterize the model
    code/               # The main estimation code, in this case StructuralEstimation.py
    figures/            # Any figures created by the main code
    tables/             # Any tables created by the main code

Because computational modeling can be very memory- and time-intensive, this file
also allows the user to choose whether to run files based on there resouce
requirements. Files are categorized as one of the following three:

- low_resource:     low RAM needed and runs quickly, say less than 1-5 minutes
- medium_resource:  moderate RAM needed and runs moderately quickly, say 5-10+ mintues
- high_resource:    high RAM needed (and potentially parallel computing required), and high time to run, perhaps even hours, days, or longer.

The designation is purposefully vague and left up the to researcher to specify
more clearly below. Using time taken on an example machine is entirely reasonable
here.

Finally, this code may serve as example code for efforts that fall outside
the HARK package structure for one reason or another. Therefore this script will
attempt to import the necessary MicroDSOP sub-modules as though they are part of
the HARK package; if that fails, this script reverts to manaully updating the
Python PATH with the locations of the MicroDSOP directory structure so it can
still run.
"""

from __future__ import annotations

import logging

from estimark.estimation import estimate
from estimark.options import (
    all_replications,
    high_resource,
    low_resource,
    medium_resource,
)

# Configure logging to show INFO level messages
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


# Ask the user which replication to run, and run it:
def run_replication():
    which_model = input(
        """Which model would you like to run?

        [1] IndShockConsumerType

         2  PortfolioConsumerType

         3  BequestWarmGlowConsumerType

         4  BequestWarmGlowPortfolioType

         5  WealthPortfolioConsumerType \n\n""",
    )

    which_replication = input(
        """Which replication would you like to run? (See documentation in do_all.py for details.) Please enter the option number to run that option; default is in brackets:

        [1] low-resource:    ~90 sec; output ./tables/estimate_results.csv

         2  medium-resource: ~7 min;  output ./figures/SMMcontour.pdf
                                             ./figures/SMMcontour.png
         3  high-resource:   ~30 min; output ./tables/bootstrap_results.csv

         4  all:             ~40 min; output: all above.

         q  quit: exit without executing.\n\n""",
    )

    subjective_markets = input(
        """Would you like to add subjective stock or labor market beliefs to the model?:

        [1] No

         2  Subjective Stock Market Beliefs

         3  Subjective Labor Market Beliefs

         4  Both\n\n""",
    )

    replication_specs = {}

    if which_model == "1" or which_model == "":
        agent_name = "IndShock"
    elif which_model == "2":
        agent_name = "Portfolio"
    elif which_model == "3":
        agent_name = "WarmGlow"
    elif which_model == "4":
        agent_name = "WarmGlowPortfolio"
    elif which_model == "5":
        agent_name = "WealthPortfolio"
    else:
        logging.error("Invalid model choice.")
        return

    if which_replication == "q":
        return

    if which_replication == "1" or which_replication == "":
        logging.info("Running low-resource replication...")
        replication_specs.update(**low_resource)

    elif which_replication == "2":
        logging.info("Running medium-resource replication...")
        replication_specs.update(**medium_resource)

    elif which_replication == "3":
        logging.info("Running high-resource replication...")
        replication_specs.update(**high_resource)

    elif which_replication == "4":
        logging.info("Running all replications...")
        replication_specs.update(**all_replications)

    else:
        logging.error("Invalid replication choice.")
        return

    if subjective_markets == "":
        subjective_markets = "1"
    if int(subjective_markets) > 1:
        agent_name += "Sub"

        if subjective_markets == "2" or subjective_markets == "4":
            agent_name += "(Stock)"
            logging.info("Adding subjective stock market beliefs...")

        if subjective_markets == "3" or subjective_markets == "4":
            agent_name += "(Labor)"
            logging.info("Adding subjective labor market beliefs...")

        agent_name += "Market"

    replication_specs["agent_name"] = agent_name
    replication_specs["save_dir"] = "docs/tables/min"

    estimate(**replication_specs)


if __name__ == "__main__":
    run_replication()

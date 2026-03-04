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

from estimark.estimation import estimate
from estimark.options import (
    all_replications,
    high_resource,
    low_resource,
    medium_resource,
)

MODEL_CHOICES = {
    "1": "IndShock",
    "": "IndShock",
    "2": "Portfolio",
    "3": "WarmGlow",
    "4": "WarmGlowPortfolio",
    "5": "WealthPortfolio",
}

REPLICATION_CHOICES = {
    "1": ("low-resource", low_resource),
    "": ("low-resource", low_resource),
    "2": ("medium-resource", medium_resource),
    "3": ("high-resource", high_resource),
    "4": ("all replications", all_replications),
}


def _build_agent_name(base_name, subjective_markets):
    """Append subjective-belief suffixes to the base agent name."""
    if subjective_markets in ("", "1"):
        return base_name

    name = base_name + "Sub"
    if subjective_markets in ("2", "4"):
        name += "(Stock)"
        print("Adding subjective stock market beliefs...")
    if subjective_markets in ("3", "4"):
        name += "(Labor)"
        print("Adding subjective labor market beliefs...")
    return name + "Market"


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

    if which_model not in MODEL_CHOICES:
        print("Invalid model choice.")
        return

    if which_replication == "q":
        return

    if which_replication not in REPLICATION_CHOICES:
        print("Invalid replication choice.")
        return

    replication_label, replication_specs = REPLICATION_CHOICES[which_replication]
    print(f"Running {replication_label} replication...")

    agent_name = _build_agent_name(MODEL_CHOICES[which_model], subjective_markets)

    estimate(**replication_specs, agent_name=agent_name, save_dir="docs/tables/min")


if __name__ == "__main__":
    run_replication()

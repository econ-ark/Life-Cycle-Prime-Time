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

import numpy as np
from HARK.ConsumptionSaving.ConsBequestModel import (
    BequestWarmGlowConsumerType,
    BequestWarmGlowPortfolioType,
)
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType
from HARK.ConsumptionSaving.ConsPortfolioModel import PortfolioConsumerType
from HARK.ConsumptionSaving.ConsWealthPortfolioModel import WealthPortfolioConsumerType
from HARK.core import AgentType

# =====================================================
# Define objects and functions used for the estimation
# =====================================================


class TempConsumerType(AgentType):
    def check_restrictions(self) -> None:
        return None

    def sim_birth(self, which_agents) -> None:
        """Alternate method for simulating initial states for simulated agents, drawing from a finite
        distribution.  Used to overwrite IndShockConsumerType.simBirth, which uses lognormal distributions.

        Parameters
        ----------
        which_agents : np.array(Bool)
            Boolean array of size self.AgentCount indicating which agents should be "born".

        Returns
        -------
        None

        """
        # Get and store states for newly born agents
        # Take directly from pre-specified distribution
        self.state_now["aNrm"][which_agents] = self.aNrmInit[which_agents]
        # No variation in permanent income needed
        self.state_now["pLvl"][which_agents] = 1.0
        # How many periods since each agent was born
        self.t_age[which_agents] = 0
        # Which period of the cycle each agents is currently in
        self.t_cycle[which_agents] = 0

    def sim_death(self):
        return np.zeros(self.AgentCount, dtype=bool)


### Overwrite sim_one_period to not have death or look up of agent ages


class IndShkLifeCycleConsumerType(TempConsumerType, IndShockConsumerType):
    """A very lightly edited version of IndShockConsumerType.  Uses an alternate method of making new
    consumers and specifies DiscFac as being age-dependent.  Called "temp" because only used here.
    """


class PortfolioLifeCycleConsumerType(TempConsumerType, PortfolioConsumerType):
    """A very lightly edited version of PortfolioConsumerType.  Uses an alternate method of making new
    consumers and specifies DiscFac as being age-dependent.  Called "temp" because only used here.
    """

    def post_solve(self) -> None:
        for solution in self.solution:
            solution.cFunc = solution.cFuncAdj


class BequestWarmGlowLifeCycleConsumerType(
    TempConsumerType,
    BequestWarmGlowConsumerType,
):
    """A very lightly edited version of BequestWarmGlowConsumerType.  Uses an alternate method of making new
    consumers and specifies DiscFac as being age-dependent.  Called "temp" because only used here.
    """


class BequestWarmGlowLifeCyclePortfolioType(
    TempConsumerType,
    BequestWarmGlowPortfolioType,
):
    """A very lightly edited version of BequestWarmGlowPortfolioType.  Uses an alternate method of making new
    consumers and specifies DiscFac as being age-dependent.  Called "temp" because only used here.
    """

    def post_solve(self) -> None:
        for solution in self.solution:
            solution.cFunc = solution.cFuncAdj


class WealthPortfolioLifeCycleConsumerType(
    TempConsumerType,
    WealthPortfolioConsumerType,
):
    """A very lightly edited version of WealthPortfolioConsumerType.  Uses an alternate method of making new
    consumers and specifies DiscFac as being age-dependent.  Called "temp" because only used here.
    """

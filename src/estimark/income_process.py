"""
This file has a modified income process constructor that adds transitory expense
shocks in retirement on top of the usual permanent-transitory shock structure.
"""

from HARK.Calibration.Income.IncomeProcesses import construct_lognormal_income_process_unemployment
from HARK.distributions.utils import add_discrete_outcome
from HARK.distributions import Lognormal, DiscreteDistribution, combine_indep_dstns, DiscreteDistributionLabeled
from copy import deepcopy
import numpy as np
from scipy.stats import norm

def construct_lognormal_income_process_with_retirement_expense_shocks(
        T_cycle,
        PermShkStd,
        PermShkCount,
        TranShkStd,
        TranShkCount,
        T_retire,
        UnempPrb,
        IncUnemp,
        UnempPrbRet,
        IncUnempRet,
        ExpShkProb,
        ExpShkMean,
        ExpShkStd,
        ExpShkCount,
        RNG,
        ):
    """
    Extension of the standard permanent-transitory income process that adds expense
    shocks in retirement, modeled as *negative* transitory income shocks. That is,
    TranShk = 1.0 - ExpShk. Expense shocks are lognormal, but only occur with given
    probability.

    Parameters
    ----------
    PermShkStd : [float]
        List of standard deviations in log permanent income uncertainty during
        the agent's life.
    PermShkCount : int
        The number of approximation points to be used in the discrete approximation
        to the permanent income shock distribution.
    TranShkStd : [float]
        List of standard deviations in log transitory income uncertainty during
        the agent's life.
    TranShkCount : int
        The number of approximation points to be used in the discrete approximation
        to the permanent income shock distribution.
    UnempPrb : float or [float]
        The probability of becoming unemployed during the working period.
    UnempPrbRet : float or None
        The probability of not receiving typical retirement income when retired.
    T_retire : int
        The index value for the final working period in the agent's life.
        If T_retire <= 0 then there is no retirement.
    IncUnemp : float or [float]
        Transitory income received when unemployed.
    IncUnempRet : float or None
        Transitory income received while "unemployed" when retired.
    ExpShkProb : float
        Probability of experiencing a non-zero expense shock in retirement.
    ExpShkMean : float
        Mean of log expense shock, relative to permanent income.
    ExpShkStd : float
        Standard deviation of log expense shock, relative to permanent income.
    ExpShkCount : int
        Number of nodes in the discretization of non-zero expense shocks.
    T_cycle :  int
        Total number of non-terminal periods in the consumer's sequence of periods.
    RNG : np.random.RandomState
        Random number generator for this type.

    Returns
    -------
    IncShkDstn :  [distribution.Distribution]
        A list with T_cycle elements, each of which is a
        discrete approximation to the income process in a period.
    """
    # First, make the standard income process
    IncShkDstnBase = construct_lognormal_income_process_unemployment(
        T_cycle,
        PermShkStd,
        PermShkCount,
        TranShkStd,
        TranShkCount,
        T_retire,
        UnempPrb,
        IncUnemp,
        UnempPrbRet,
        IncUnempRet,
        RNG,
    )
    
    # Make the distribution of expense shocks
    CritShk = -ExpShkMean / ExpShkStd  # expenses > income
    CDFbounds = [0., norm.cdf(CritShk)]
    ExpShkDstnBase = Lognormal(ExpShkMean, ExpShkStd).discretize(ExpShkCount, tail_bound=CDFbounds, tail_N=1)
    ExpShkDstnBase.atoms[0,-1] = 1.
    ExpShkDstn = add_discrete_outcome(ExpShkDstnBase, 0.0, 1.0-ExpShkProb)
    
    # Translate the expense shock distribution into a transitory income distribution
    TranShkDstnRet = deepcopy(ExpShkDstn)
    TranShkDstnRet.atoms -= 1.
    TranShkDstnRet.atoms *= -1.
    #AvgNetIncRet = np.dot(TranShkDstnRet.atoms[0,:], TranShkDstnRet.pmv)
    #TranShkDstnRet.atoms /= AvgNetIncRet
    TranShkDstnRet.atoms = np.abs(TranShkDstnRet.atoms)
    
    # Combine that transitory shock distribution with a trivial permanent shock dstn
    PermShkDstnRet = DiscreteDistribution(pmv=np.array([1.0]), atoms=np.array([1.0]))
    IncShkDstnRet = combine_indep_dstns(PermShkDstnRet, TranShkDstnRet)
    IncShkDstnRet = DiscreteDistributionLabeled.from_unlabeled(IncShkDstnRet,
                                                               name="Retired income shock distribution",
                                                               var_names=["PermShk","TranShk"])
    
    # Take income distributions during the working life
    IncShkDstn = []
    for t in range(T_retire):
        IncShkDstn.append(IncShkDstnBase[t])
    
    # Replace the income shock distribution in each year of retirement
    for t in range(T_retire, T_cycle):
        seed_t = RNG.integers(0, 2**31 - 1)
        IncShkDstnRet_t = deepcopy(IncShkDstnRet)
        IncShkDstnRet_t.seed = seed_t
        IncShkDstn.append(IncShkDstnRet_t)
        
    return IncShkDstn


def construct_lognormal_income_process_with_mateos_expense_shocks(
        T_cycle,
        PermShkStd,
        PermShkCount,
        TranShkStd,
        TranShkCount,
        T_retire,
        UnempPrb,
        IncUnemp,
        UnempPrbRet,
        IncUnempRet,
        RNG,
        ):
    """
    Extension of the standard permanent-transitory income process that adds expense
    shocks in retirement, modeled as *negative* transitory income shocks. That is,
    TranShk = 1.0 - ExpShk. Expense shocks are lognormal, but only occur with given
    probability.

    Parameters
    ----------
    PermShkStd : [float]
        List of standard deviations in log permanent income uncertainty during
        the agent's life.
    PermShkCount : int
        The number of approximation points to be used in the discrete approximation
        to the permanent income shock distribution.
    TranShkStd : [float]
        List of standard deviations in log transitory income uncertainty during
        the agent's life.
    TranShkCount : int
        The number of approximation points to be used in the discrete approximation
        to the permanent income shock distribution.
    UnempPrb : float or [float]
        The probability of becoming unemployed during the working period.
    UnempPrbRet : float or None
        The probability of not receiving typical retirement income when retired.
    T_retire : int
        The index value for the final working period in the agent's life.
        If T_retire <= 0 then there is no retirement.
    IncUnemp : float or [float]
        Transitory income received when unemployed.
    IncUnempRet : float or None
        Transitory income received while "unemployed" when retired.
    T_cycle :  int
        Total number of non-terminal periods in the consumer's sequence of periods.
    RNG : np.random.RandomState
        Random number generator for this type.

    Returns
    -------
    IncShkDstn :  [distribution.Distribution]
        A list with T_cycle elements, each of which is a
        discrete approximation to the income process in a period.
    """
    # First, make the standard income process
    IncShkDstnBase = construct_lognormal_income_process_unemployment(
        T_cycle,
        PermShkStd,
        PermShkCount,
        TranShkStd,
        TranShkCount,
        T_retire,
        UnempPrb,
        IncUnemp,
        UnempPrbRet,
        IncUnempRet,
        RNG,
    )
    
    # Copy Mateo's college-educated expense shock distribution. This is extremely
    # poor formatting, but we're pressed on time so too bad.
    equiprobable_one_seventh = np.ones(7) / 7.
    exp_shks_65_to_69 = np.array([0.003, 0.010, 0.019, 0.031, 0.050, 0.089, 0.227])
    exp_shks_70_to_74 = np.array([0.004, 0.013, 0.024, 0.039, 0.060, 0.103, 0.262])
    exp_shks_75_to_79 = np.array([0.004, 0.015, 0.028, 0.047, 0.074, 0.123, 0.294])
    exp_shks_80_to_84 = np.array([0.004, 0.017, 0.033, 0.054, 0.089, 0.155, 0.410])
    exp_shks_85_to_89 = np.array([0.002, 0.015, 0.033, 0.057, 0.100, 0.191, 0.719])
    exp_shks_90_plus  = np.array([0.000, 0.015, 0.039, 0.075, 0.160, 0.389, 1.000])
    exp_shks_retired =  5*[exp_shks_65_to_69] + \
                        5*[exp_shks_70_to_74] + \
                        5*[exp_shks_75_to_79] + \
                        5*[exp_shks_80_to_84] + \
                        5*[exp_shks_85_to_89] + \
                        31*[exp_shks_90_plus]
                        
    # Take income distributions during the working life
    IncShkDstn = []
    for t in range(T_retire):
        IncShkDstn.append(IncShkDstnBase[t])
        
    # Add the "net income" distributions when retired
    for t in range(T_retire, T_cycle):
        seed_t = RNG.integers(0, 2**31 - 1)
        s = t - T_retire
        PermShkDstn_t = DiscreteDistribution(pmv=np.array([1.0]), atoms=np.array([1.0]))
        TranShkDstn_t = DiscreteDistribution(pmv=equiprobable_one_seventh, atoms=1-exp_shks_retired[s])
        IncShkDstn_t = DiscreteDistributionLabeled.from_unlabeled(combine_indep_dstns(PermShkDstn_t, TranShkDstn_t, seed=seed_t),
                                                                   name="Retired income shock distribution",
                                                                   var_names=["PermShk","TranShk"])
        IncShkDstn.append(IncShkDstn_t)
        
    return IncShkDstn
    
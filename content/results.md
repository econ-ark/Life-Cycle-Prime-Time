@parameters shows the results of our estimation exercise.
For the standard Life-Cycle-Portfolio (LCP) model, we estimate a CRRA $\CRRA$ coefficient of about 8.8, which lines up with the literature finding that portfolio choice models require a very high $\CRRA$ in order to prevent agents from putting all their assets in the risky form.
The Warm-Glow Portfolio Choice model also estimates a $\CRRA$ coefficient that also rounds to 8.8.
as well as a bequest factor $\alpha$ of about 44, and a bequest shifter $\underline{a}$ of 26.
The fact that the $\CRRA$ parameter is nearly unchanged is a clue to something that we will see in our figures: Although the bequest factor $\alpha$ is large, the estimated bequest shifter $\underline{a}$ is also large enough that it renders the bequest motive almost irrelevant for the median college-educated household we are examining.
This is consistent with previous findings in the literature such as those by @deNardiBequest, who finds that the bequest motive comes into play only for the richest households.
Finally, the TRP Portfolio Choice model estimates a CRRA $\CRRA$ coefficient of 3.472 and a wealth share of utility $\delta$ coefficient of 0.531.
This result is significant because the CRRA $\CRRA$ coefficient required to match the wealth accumulation patterns is significantly lower than that of the Standard Life-Cycle Portfolio choice model, whose high CRRA $\CRRA$ has long been a puzzle in the literature.
The addition of a non-separable utility of wealth factor $\delta$ allows the TRP Portfolio model to match the wealth accumulation patterns with a lower CRRA $\CRRA$ coefficient, which is more in line with the literature on risk aversion.
Finally, we can observe the column labeled "Criterion", which represents the minimum value of the objective function attained for each model during the estimation process.
The TRP Portfolio model has the lowest criterion value, indicating that it is the best-fitting model among the three.

```{include} parameters.tex
```

%% MNW: I have some serious concerns about these results. First, the Warm-Glow model results are essentially identical to the basic Life-Cycle model: the criterion is identical down to the third digit, and all of the simulated moments appear identically placed-- I can't tell them apart. If you go from a model with one free parameter to one with three free parameters (which embeds the first), and the criterion function changes by less than 0.1% even though the new parameter values are *far* from their implied baseline value (zero)... there's a problem. At the very least, the bequest motive parameters *are not identified at all*: if you tried to construct standard errors, they'd be hundreds (or thousands) of times *bigger* than the parameter estimates. My suspicion is that something isn't right about the estimation, and those parameters weren't properly estimated at all.

%% MNW: Beyond that, I don't think there's sufficient variation / information in the moments to credibly identify the bequest shifter. The shifter makes the bequest motive matter more for agents with high wealth-to-income ratios than for low ones. But a) you don't make moments based on that; and b) without ex ante heterogeneity, there might not be enough variation in aNrm to meaningfully do that anyway.

@medshare shows the median portfolio share for the agents in our simulation, along with the target share moments that come from @Aboagye2024.
That paper presents the typical glide-path of target-date funds (TDFs) which provide a basis for much of commercial financial advice.
While the red line shows the whole life-cycle glidepath of optimal advice, here we only target those moments starting at age 70.
As we can see, the TRP Portfolio model does a good job of matching the targeted portfolio shares post-retirement, while the Life-Cycle Portfolio and the Warm-Glow Portfolio models come close but persistently under-estimate the share of risky assets.

%% MNW: Here, it looks like the green line (TRP model) is perfectly flat, while the other two are declining slightly with age. Why is that? It makes me worry that all forms of risk were turned off in the TRP model, resulting in a constant risk share.

```{figure} figures/median_share
:label: medshare
:align: center 

Median Portfolio Share for different portfolio models. The red line shows the target moments from @Aboagye2024. 
```

%% MNW: All of the models are vastly overshooting wealth accumulation at younger ages, and this is *especially* the case for the young population. You used constant weights on the moments by age, but if you used their empirical (inverse) variances, the green path *would not* fit better than the other model paths. Of course, the estimation would have produced a different set of parameters and different moment fit with those weights. But from an eyeball test, the green one doesn't look meaningfully "better" to me.

%% MNW: Also note that For the LC and WG models, you're overshooting wealth ratios when young, and undershooting risky portfolio shares when young. You're only undershooting wealth ratios for the two highest moments. Rho is your *only* free parameter, and lower wealth ratio can be achieved with lower rho. Higher risky asset share can also be achieved with lower rho. I'm a little incredulous that 15 moments wanting rho to go down and 2 wanting rho to go up results in this balance.

@medwealth shows the median wealth to income ratio[^wtoy] for achieved during the simulation.
Again, the red line represents the target wealth to income ratios, or the empirical moments of our simulation, that come from the Survey of Consumer Finances.
One might be concerned about the presence of a "zig-zag" in the aggregate empirical data, but this is likely due to selection/sampling bias and the reduction of participating households at higher ages due to death.
The Life-Cycle and Warm-Glow Portfolio models overshoot the wealth accumulation over the life-cycle, but as expected, the agents in these simulations start to run down their wealth right after retirement.
The TRP Portfolio model similarly overshoots wealth accumulation for working-age agents, but the agents in this simulation do not run down their wealth post-retirement.
Overall, the TRP Portfolio model does a good job of matching the observed pattern post-retirement for the median household: peak of wealth to income accumulation post-retirement and a slow decline in the wealth to income ratio after that.

%% MNW: What is the "selection/sampling" bias? There *are* fewer households in the SCF at those old ages, which would be accounted for with appropriate moment weights.

[^wtoy]: Wealth is `networth` and income consists of wages, social security, and retirement income as defined by the Survey of Consumer Finances.

```{figure} figures/median_wealth
:label: medwealth
:align: center 

Median Wealth to Income Ratio for different portfolio models. The red line indicates median wealth-to-income ratios for College educated households in the Survey of Consumer Finances. Wealth is `networth` and income consists of wages, social security, and retirement income. 
```

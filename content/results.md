@parameters shows the results of our estimation exercise.
For the standard Life-Cycle-Portfolio (LCP) model, we estimate a CRRA $\CRRA$ coefficient that rounds to 8.8, which lines up with the literature finding that portfolio choice models requiring a very high $\CRRA$ in order to prevent agents from putting all their assets in the risky form.
The Warm-Glow Portfolio Choice model estimates a CRRA $\CRRA$ coefficient of that also rounds to 8.8.
While it also estimates a bequest factor $\alpha$ of about 44, and a bequest shifter $\underline{a}$ of 26.
The fact that the $\CRRA$ parameter is nearly unchanged is a clue to something that we will see in our figures: Although the bequest factor $\alpha$ is large, the estimated bequest shifter $\underline{a}$ is also large enough that it renders the bequest motive almost irrelevant for the median college-educated household we are examining.
This is consistent with previous findings in the literature such as those by @deNardiBequest, who finds that the bequest motive comes into play only for the richest households.
Finally, the TRP Portfolio Choice model estimates a CRRA $\CRRA$ coefficient of 3.472 and a wealth share of utility $\delta$ coefficient of 0.531.
This result is significant because the CRRA $\CRRA$ coefficient required to match the wealth accumulation patterns is significantly lower than that of the Standard Life-Cycle Portfolio choice model, whose high CRRA $\CRRA$ has long been a puzzle in the literature.
The addition of a non-separable utility of wealth factor $\delta$ allows the TRP Portfolio model to match the wealth accumulation patterns with a lower CRRA $\CRRA$ coefficient, which is more in line with the literature on risk aversion.
Finally, we can observe the column labeled "Criterion", which represents the minimum value of the objective function attained for each model during the estimation process.
The TRP Portfolio model has the lowest criterion value, indicating that it is the best-fitting model among the three.

```{include} parameters.tex
```

@medshare shows the median portfolio share for the agents in our simulation, along with the target share moments that come from @Aboagye2024.
That paper presents the typical glide-path of target-date funds (TDFs) which provide a basis for much of commercial financial advice.
While the red line shows the whole life-cycle glidepath of optimal advice, here we only target those moments starting at age 70.
As we can see, the TRP Portfolio model does a good job of matching the targeted portfolio shares post-retirement, while the Life-Cycle Portfolio and the Warm-Glow Portfolio models come close but persistently under-estimate the share of risky assets.

```{figure} figures/median_share
:label: medshare
:align: center 

Median Portfolio Share for different portfolio models. The red line shows the target moments from @Aboagye2024. 
```

@medwealth shows the median wealth to income ratio[^wtoy] for achieved during the simulation.
Again, the red line represents the target wealth to income ratios, or the empirical moments of our simulation, that come from the Survey of Consumer Finances.
One might be concerned about the presence of a "zig-zag" in the aggregate empirical data, but this is likely due to selection/sampling bias and the reduction of participating households at higher ages due to death.
The Life-Cycle and Warm-Glow Portfolio models overshoot the wealth accumulation over the life-cycle, but as expected, the agents in these simulations start to run down their wealth right after retirement.
The TRP Portfolio model similarly overshoots wealth accumulation for working-age agents, but the agents in this simulation do not run down their wealth post-retirement.
Overall, the TRP Portfolio model does a good job of matching the observed pattern post-retirement for the median household: peak of wealth to income accumulation post-retirement and a slow decline in the wealth to income ratio after that.

[^wtoy]: Wealth is `networth` and income consists of wages, social security, and retirement income as defined by the Survey of Consumer Finances.

```{figure} figures/median_wealth
:label: medwealth
:align: center 

Median Wealth to Income Ratio for different portfolio models. The red line indicates median wealth-to-income ratios for College educated households in the Survey of Consumer Finances. Wealth is `networth` and income consists of wages, social security, and retirement income. 
```

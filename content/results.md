@medshare shows the median portfolio share for the agents in our simulation, along with the target share moments that come from @Aboagye2024. While the red line shows the whole life-cycle glidepath of optimal advise, here we only target those moments starting at age 70. As we can see, the TRP Portfolio model does a good job of matching the targeted portfolio shares post-retirement, while the Life-Cycle Portfolio and the Warm-Glow Portfolio models come close but persistently under-estimate the share of risky assets.

```{figure} figures/median_share
:label: medshare
:align: center 

Median Portfolio Share for different portfolio models. The red line shows the target moments from @Aboagye2024. 
```

@medwealth shows the median wealth to income ratio[^wtoy] for achieved during the simulation. The Life-Cycle and Warm-Glow Portfolio models overshoot the wealth accumulation over the life-cycle, but as expected, the agents in these simulations start to run down their wealth right after retirement. The TRP Portfolio model similarly overshoots wealth accumulation for working-age agents, but the agents in this simulation do not run down their wealth post-retirement. Overall, the TRP Portfolio model does a good job of matching the observed pattern post-retirement for the median household: peak of wealth to income accumulation post-retirement and a slow decline in the wealth to income ratio after that.

[^wtoy]: Wealth is `networth` and income consists of wages, social security, and retirement income as defined by the Survey of Consumer Finances.

```{figure} figures/median_wealth
:label: medwealth
:align: center 

Median Wealth to Income Ratio for different portfolio models. The red line indicates median wealth-to-income ratios for College educated households in the Survey of Consumer Finances. Wealth is `networth` and income consists of wages, social security, and retirement income. 
```

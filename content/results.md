@parameters shows the results of our estimation exercise, and the fit of the three estimated models is plotted below, in @medwealth and @medshare.

```{include} parameters.tex
```

For the standard Life-Cycle Portfolio (LCP) model, we estimate a CRRA $\CRRA$ coefficient of about 8, which lines up with the literature finding that portfolio choice models require a very high $\CRRA$ in order to prevent agents from putting all their assets in the risky form.
In general, "typical" values for the CRRA coefficient (from experimental evidence and other contexts) are considered to be between 1 and 5.
The "criterion" column of @parameters lists the minimum value that the objective function achieves for each model-- the smallest weighted squared distance between simulated moments and empirical moments.
The LCP model performs poorly by this measure, as illustrated in the figures.
LCP consumers want to quickly run down their wealth at older ages, as the probability of death increases with age and they know that they "can't take it with them."
To try to match the observed empirical wealth trend (red dashed line in @medwealth), which holds steady at a high wealth-to-income ratio at older ages, the LCP model (solid blue line) exceeds observed wealth accumulation through the working life.
Even then, the wealth drawdown is so rapid that the best the LCP model can achieve is to significantly overshoot wealth before age 65, and then vastly undershoot it in retirement.

```{figure} figures/median_wealth
:label: medwealth
:align: center 

Median Wealth to Income Ratio for different portfolio models. The red line indicates median wealth-to-income ratios for College educated households in the Survey of Consumer Finances. Wealth is `networth` and income consists of wages, social security, and retirement income. 
```

As discussed above, there are multiple model features that can ameliorate or eliminate the wealth drawdown problem, beginning with a simple bequest motive.
The Warm-Glow Portfolio model (orange lines on figures) estimates a much more realistic CRRA coefficient of $\CRRA = 4.65$.
With a strong bequest motive, the Warm-Glow model is able to match the high levels of wealth observed deep into retirement.
That is, these consumers do not quickly draw down their assets because they take great pleasure in passing their estate on to their heirs.
The bequest motive magnitude $\alpha$ and shifter term $\underline{a}$ cannot be *directly* interpreted in human terms, instead requiring an indirect interpretation used in @DeNardi2010 (see their Appendix D).
Consider the extreme case of a model consumer who is *so old* that they can't possibly survive to the next period-- age 120, in our calibration.
Facing certain imminent death, how much should this person consume versus allocate to their bequest?
The form of the warm-glow bequest motive dictates that the optimal mapping from cash-on-hand to consumption is piecewise linear with a single kink: below a certain threshold wealth-to-income ratio, they should *consume all resources*, and then allocate to their bequest a *constant fraction* of any wealth above the threshold.
The estimated $\alpha$ and $\underline{a}$ can be mathematically transformed to find a "bequest threshold" of about 0.43 and a "marginal propensity to bequeath" of 0.875; that is, a terminally old agent will allocate to their bequest 87.5\% of any wealth above 43\% of their permanent income.
This strong bequest motive at the very end of life propagates backward to more reasonable ages (albeit not as readily quantifiable), and ultimately it applies for essentially *everyone*.
In contrast, the literature has generally found (e.g. @deNardiBequest) that the bequest motive comes into play only for relatively wealthy households, and is mostly inoperative around median wealth.
This discrepancy might arise because of the simplified approach we have used here, matching *only* the median wealth-to-income ratio by age, rather than wealth levels conditional on income.

Digging deeper, the Warm-Glow model predicts that saving behavior *when young* is strongly motivated by the bequest motive.
Recall from the discussion of the [Survey of Consumer Finances](https://doi.org/10.17016/8799) and @jaherGilded that very few older people ascribe their wealth-holding behavior to a bequest motive, and yet the Warm-Glow model has the saving choices of *40 year olds* driven by the urge to bequeath.
Even if a model can *mechanically* reproduce observed data features or hit empirical targets, that does not make it "right" or "true," especially if its underlying logic is implausible and contradictory to qualitative evidence.
And as discussed above, the bequest motive is inconsistent with an investment advisor's fiduciary duty *to the client*.
We include the Warm-Glow model in our presentation not to advocate for it, but merely to demonstrate that there are *multiple ways* for life-cycle models to generate more realistic wealth trajectories in retirement.

```{figure} figures/median_share
:label: medshare
:align: center 

Median Portfolio Share for different portfolio models. The red line shows the target moments from @Aboagye2024. 
```

Our preferred specification also has the agents value wealth itself as a motivation to retain assets later in life, but in a way that is more consistent with qualitative responses.
The Wealth-in-Utility-Function (WIUF) / TRP Portfolio model estimates a CRRA $\CRRA$ coefficient of about 4.88 and a wealth share of utility $\delta$ coefficient of 0.16.
This result is significant because the CRRA $\CRRA$ coefficient required to match the wealth accumulation patterns is significantly lower than that of the standard Life-Cycle Portfolio choice model, whose high CRRA $\CRRA$ has long been a puzzle in the literature.
As seen in @medwealth, the WIUF / TRP model (green line) does not need to overshoot wealth accumulation in early life by nearly as much as the basic LCP model, as agents want to retain assets in retirement to generate utility directly.
Compared to the Warm-Glow model, the WIUF / TRP specification does predict more wealth accumulation early in life, but for more immediate reasons: young consumers value money and liquidity *now*, rather than saving at age 35 to leave a large bequest at age 85.

Moreover, because the CRRA parameter doesn't need to be so high, the WIUF model can better match the target risky assets share moments (red dashed line in @medshare), which come from @Aboagye2024. 
That paper presents the typical glide-path of target-date funds (TDFs) which provide a basis for much of commercial financial advice.
While the whole life-cycle glidepath is provided in @Aboagye2024, here we only target (and plot) those moments starting at age 70.
The model fit with respect to risky asset share is comparable for the Warm-Glow model, generally matching the level and recommended shallow downward slope.
The basic LCP model, however, badly fits the risky asset share too low due to the high $\CRRA$ value needed in its attempt to match the life-cycle wealth pattern.

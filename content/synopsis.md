---
title: Synopsis
exports:
    - format: tex+pdf
      template: arxiv_nips
      output: synopsis.pdf
    - format: docx
      template: default
      output: synopsis.docx
---

# Synopsis 

The retirement planning landscape is evolving rapidly due to shifting demographics, longer life expectancy, and financial innovation. As retirees live longer, the need for retirement plans to provide flexible, rigorous, and sustainable financial advice has become increasingly urgent.

But economists' traditional "life-cyle" model gives deeply unappealing advice ('invest all your wealth in the stock market;' 'after retirement, run down your wealth to zero then live pension-check to pension-check'). These shortcomings have meant that financial advisors could not ground their financial advice in transparent economic reasoning.

Fortunately, recent advances in theory and (especially) computation have given rise to a new generation of tools — 'estimated structural models' — that can finally bridge the gap between theory and sound real-world advice.

This report demonstrates the point: We leverage these developments to construct a completely rigorous model that can give advice that seems sensible to professionals. And, because of its rigorous construction principles, its recommendations can also be customized ('how should I behave if I am more risk averse than normal?').

## Key Insights from the Model 

- **Wealth Preservation Post-Retirement**: Using either of two variants, our framework robustly concludes that retirees place a high premium on wealth preservation in retirement. But its advice is not one-size-fits-all; it accounts, for example, for the fact that unpredictable unavoidable expenses may make wealth preservation impossible (or undesirable).

- **Dynamic Asset Allocation**: An intrinsic desire to hold onto wealth enhances the lure of the (usually) high returns historically offered by stocks. But investing most or all of your wealth in stocks puts your future financial security at risk.  Our models calculates the investment plans that mathematically balance the lure and the danger.  The proper balance depends on the degree of the typical consumer's aversion to risk (taking into account other sources of risk aside from stock returns).  The structural model finds risk preferences for which the traditional 'glide paths' recommended by financial advisors are appropriate. It can provide advice tailored to people with greater or less risk aversion than average.

- **Pre-Retirement Behavior Informs Choices in Retirement**: Some financial planning tools treat retirees as if they are born on the day of their retirement, with no prior history.  Our modeling results demonstrate that preretirement behavior places powerful constraints on what can plausibly be considered optimal for the same consumer post-retirement.

## Further Applications 

An emerging frontier in the financial advising industry is to move beyond 'one-size-fits-all' recommendations toward advice that is tailored to each person's particular circumstances.

This is precisely what our modeling approach already does: It keeps track of the evolution of each person's circumstances and constructs a plan that is optimal for that particular consumer. Our fundamental modeling strategy can accommodate many further degrees of refinement, including a richer variety of investment options, incorporating a spouse/partner's finances, specialization to give advice appropriate to particular industries or occupations, and much more.

This customizability is the result of our choice to build [our model](https://github.com/econ-ark/life-cycle-prime-time) model using the [open-source software](https://en.wikipedia.org/wiki/Open-source_software) [HARK](https://docs.econ-ark.org) toolkit. This approach makes it vastly easier to inspect, understand, extend, expand, or modify the computer code that generates the results. 

Our model demonstrates that it is finally possible to construct believable financial advice based on rigorous economic reasoning. This offers the prospect that financial advice can be understood and stress-tested much more easily than is currently possible, building a solid foundation of trust for the industry as a whole.

+++

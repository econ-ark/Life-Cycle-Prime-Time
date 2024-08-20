---
title: Life Cycle Modeling is (Almost) Ready for Prime Time
exports:
    - format: tex+pdf
      template: arxiv_nips
      output: life-cycle-prime-time.pdf
---

%% [ ] AL: Remind me - we are now incorporating aggregate productivity growth of 1.5 percent/yr?
%% [ ] AL: Need to import Mateo's medical expense shocks (and need to make them a default option in the life cycle models in HARK)


+++ { "part": "abstract" }

The 'life cycle model' of optimal saving for retirement is familiar to anyone who has taken an introductory economics class. When hiring a financial advisor, people probably think the advisor's job is just to tailor optimal life-cycle-model choices to their particular circumstances. But academics and financial advisors know that the advice (about both saving and portfolio choice) provided by standard academic life-cycle models is deeply problematic -- for example, most such models imply that retirees should plan to run their wealth down to zero or some small amount and then (optimally!) live pension-check to pension-check (at least approximately). This paper makes the case that recent developments in the economics literature have finally given us the tools we need to construct rigorous life cycle models whose advice is sensible.  We provide one example of a simple model that can solve a number of problems with the standard model by putting wealth in the utility function.

+++

# Introduction

Franco Modigliani and Richard Brumberg (1954)[^modigliani_brumberg] were the first to propose trying to understand consumer financial choices as reflecting optimal responses to the realities of the path of income and of spending needs over the lifetime. An enormous academic literature has followed that pioneering work, but it has proven difficult to build rational optimizing models that give sensible advice about both life cycle saving choices and about investment decisions like how much of one's retirement savings should be invested in the stock market.

[^modigliani_brumberg]: @10.7551/mitpress/1923.003.0004

But in the last few years, the academic literature has developed in ways that offer the prospect that we may now finally be able to build rigorous optimizing life cycle models whose advice is not obviously wrong.

### Computation/Uncertainty/Complexity 

The first such development is the rapid advance of computational capacity, which has made it possible to dispense with inappropriate simplifications and to construct credible answers to the question "what saving and portfolio choices are truly mathematically optimal" in a real world whose key complexities can finally be handled appropriately. In particular, the incorporation of realistic descriptions of the uncertainties decisionmakers face (about their own income, stock returns, interest rates, health expenditures, mortality, and more) makes computation of the optimal solution astonishingly difficult. Much harder, say, than the computation of optimal trajectories for spacecraft; comparable perhaps to the computational difficulty of figuring out how to drive a car roughly as well as a human (another problem where adequate computational solutions have only recently become available).

### Survey Data on Expectations and Preferences

A second academic development has been a new openness to the idea that people's beliefs and preferences can be probed by *asking them* about their beliefs and preferences.

In the context of motivations for saving, this leads us to want to take seriously the answers to a survey question about their 'most important' reason for saving that respondents to the Federal Reserve's [Survey of Consumer Finances (SCF)](https://www.federalreserve.gov/econres/scfindex.htm) have been asked for many years. Among retirees, one answer dominates the rest: 'Liquidity/The Future.'  (See [the discussion below](#most-important-reason) for details).

The 'Liquidity' component of this answer suggests the possibility that precautionary saving motives matter for many households -- highlighting the essential nature of abovementioned computational advancements.

The traditional approach to calibrating such models has been for economists to try to construct objective measurements of the necessary information (like stock returns), and to assume that households believe whatever it is that the economist has measured. But among the information newly being collected in surveys are data on expectations; and it turns out that economists' constructed beliefs often differ greatly from the beliefs that many people actually hold.  It seems reasonable to suppose that the decisions people make reflect their own beliefs rather than whatever it is that economists think they *should* believe.

% And, rather than being constant with age as economists typically assume, @albert2012differences provide evidence that risk aversion increases with age.

Some early work suggests that taking these new calibrations into account could resolve some of the problems that have traditionally beset the life cycle modeling literature. For example, Mateo @velasquezgiraldoJMP has shown that even college-educated people systematically have held beliefs about stock market returns that are pessimistic compared to the returns the market has historically delivered. He argues that this explains why, historically, people have been less eager to invest in stocks than would be predicted by models calibrated with economists' more optimistic expectations. It turns out that the portfolio investment behavior of college-educated people over most of their lives is reasonably consistent with rational decisionmaking -- given their measured beliefs.  To put it bluntly, the surveys find that many people think that investment in stocks is a lousy deal - low return and high risk.  It's no mystery why such people do not invest.

It is not exactly shocking that many people hold beliefs that differ from those of experts -- especially on subjects (like the returns and risk stock investments) whose mastery requires meaningful domain-specific education. Presumably, this is why there is a large industry offering financial advice: many people are not confident that they understand everything necessary to make good financial financial choices on their own. 

The provision of financial advice, however, is fraught with potential conflicts of interest. That is why the idea of justifying that advice with an explicit and transparent mathematical modeling framework is so attractive. If the advisor's advice is consistent with the model, and the model can be checked both for mathematical correctness and conceptual soundness (by outside experts), then it is reasonable for a client hiring an advisor to trust that advice.

### Model Specification and Estimation 

In the [Models](#Models) section of the paper, we provide a formal description of the mathematical and computational structure of our optimizing models, beginning with the standard Life Cycle Portfolio model (which computes optimal saving and portfolio shares over the life cycle).  We will find, in the [Estimation](#Estimation) section of the paper, that the model implies a rapid drawdown of wealth after retirement that we simply do not see, confirming a longstanding problem with basic life cycle models (see, e.g., @hurd1987savings).[^AmeriksCaveat]  (The 'drawdown failure': People fail to draw down their wealth).  We next describe a model in which consumers have a bequest motive, because the literature has explored whether such a motive could explain the drawdown failure.  But in the [Estimation](#Estimation) section we confirm the consensus in the literature that the bequest motive does not seem to have much force for the median household.

[^AmeriksCaveat]: Some impressive recent work by Ameriks, Caplin, and coauthors (@ameriks2011joy, @Ameriks2020jpe) has argued that concerns about the possibility of extremely large medical costs -- for example for nursing home care -- may be behind the drawdown failure for some people. Although our model attempts to take medical expenditure shocks into account, it is not calibrated with the @Ameriks2020jpe medical shocks; it would be interesting to see how our results might change if we were to do so.

This leads us into more speculative territory.  If what consumers care most about is to hold wealth for 'Liquidity/The Future' but that wealth is not explainable by a precautionary motive springing from measurable risks, a potential interpretation is that consumers value the ownership of wealth in and of itself.  After fleshing out this idea a bit, we propose an alternative model that puts wealth in the utility function directly -- and in the [Estimation](#Estimation) section we compare the predictions of this model to those of the standard Life Cycle Portfolio model and its extension that allows for bequests.

The main quantitative/mathematical result of this paper is to show that such a model with 'wealth in the utility function' can fit observed post-retirement behavior of both wealth-holding and portfolio choice better than the standard model (with or without a bequest motive).[^college]

[^college]: We focus on college educated households partly because a growing body of literature - including @velasquezgiraldoJMP's work cited above -- finds that the behavior of the college-educated population comes much closer to matching the predications of optimizing models than the behavior of people with less education).

But the broader point is that, recently, our modeling and conceptual tools (including the idea that softer data like surveys should be taken seriously) have advanced to the point where it is finally possible to construct rational optimizing models of life cycle financial choice that can serve as a credible justification for normative advice.

# Models

The academic literature on life cycle modeling is extraordinarily rich, and we cannot hope to do justice to it here. What we have done instead is to construct a 'toy model' that captures some key points and ideas. We think of this as a starting point for what we hope will be a new literature that aims to integrate insights from many different kinds of evidence into a plausible framework for thinking realistically about life cycle financial choice.

One kind of further evidence that we view as vital is the experience of financial advisors themselves in interactions with their clients. We have been told,[^nodrawdown] for example, that advice that clients should run their wealth down to zero then live pension-check to pension-check would be so unwelcome that a financial advisor who provided that advice would be fired.

[^nodrawdown]: Personal communication, James Tzitzouris with Christopher Carroll, 2024-05-15.

The kinds of models we are examining here are well suited to the task of crafting systematic advice for clients like employers who need to hire 401(k) plan providers. It is not hard to imagine that such employers might be attracted to a 401(k) provider whose advice is justified by, and can be explained using the logic of, a well-specified model of optimal choice.  That might be more persuasive than 'trust us, we know what we are doing.'

For purposes like 401(k) or other pension plan design, the optimization problem can be constrained to one that satisfies the legal obligations the employers have to their employees. For example, the employer's contract is with the employee, not with the employee's heirs. The employer's duty is to craft a plan that is expected to permit the employee to have adequate resources for their own expenditures during retirement. These legal considerations effectively prohibit the advisor from including a bequest motive in its optimization objective.[^planprovideradvantage]

[^planprovideradvantage]: One way to accommodate this requirement would be to limit the empirical sample used to estimate the model to childless people. This might not be feasible with public datasets like the SCF because the sample sizes might be too small; but with large administrative data of the kind available to 401(k) providers it should be possible.

## The Baseline Academic Models

### The Life Cycle Portfolio ('LCP') Model

We begin by describing the optimal consumption/saving problem over the life cycle for a consumer with no access to a risky asset (like the stock market) that earns a higher (expected) rate of return than the safe asset. After we have finished describing the plain life cycle model we will augment it to add optimal portfolio choice between safe and risky assets.

In each period, a consumer's flow of utility depends on how much they consume. We assume that the utility function is of the standard Constant Relative Risk Aversion form:
\begin{align}
    \uFunc(c) & = \frac{c^{1-\CRRA}}{1-\CRRA}
\end{align}
but of course the consumer is smart enough to realize that preserving some resources for the future is a good idea; this is why all wealth is not consumed immediately.

We follow a tradition dating back to @friedman1957 in assuming that a consumer's financial circumstances depend chiefly on two variables. $\pLvl_{t}$ is the consumer's permanent income (roughly, the income they would normally expect to receive in the absence of surprises like winning the lottery or a temporary layoff), while $\mLvl_{t}$ is total market resources (the sum of financial assets and current income -- think of this as the pool of resources that can be immediately spent; 'money' in the colloquial sense of 'how much money does grandma have?').

The 'value' of having a given amount of market resources $\mLvl_{t}$ right now, and of knowing your current permanent income level to be $\pLvl_{t}$, is determined by the utility you will experience from consumption today, as well as the utility you expect to experience in the future. Any future period matters to you only to the extent that you expect to survive to that period. 

In formal mathematical terms, the consumer's objective is to maximize present discounted utility from consumption over a life cycle that ends no later than date $T$ (often set to age 120):

\begin{equation}
    \pmb{\vFunc}_{t}(\mLvl_{t},\pLvl_{t}) = \max_{\{\cFunc\}_{t}^{T}} ~ \uFunc(\cLvl_{t})+\Ex_{t}\left[\sum_{n=1}^{T-t} \Alive_{t}^{t+n}{\DiscFac}^{n} \uFunc(\cLvl_{t+n}) \right] \label{eq:lifecyclemax}
\end{equation}

\begin{align}
    \\ \Alive _{t}^{t+n} & : \text{probability to } \Alive \text{ive until age $t+n$ given you are alive at age $t$}
    \\                   & {~~~}\bullet \Alive_{120}^{121} = 0.0 \text{ says that a 120 year old has zero probability of living to 121}
    \\                   & {~~~}\bullet \Alive_{80\phantom{1}}^{90\phantom{1}} = 0.3 \text{ says that an 80 year old has a 30 percent chance of reaching 90}
    \\ \DiscFac = 1        & : \text{time discount factor (captures degree of present bias)}
\end{align}

We use standard calibrations for mortality by age from actuarial mortality tables used by the Social Security administration. We set the 'pure' rate of time preference to $\beta=1$ because that means that the optimal choice is to care exactly as much your future self as much as your present self (conditional on surviving into the future). 

One of the fundamental discoveries of the past 40 years or so is the extent to which optimal choice is profoundly altered by the presence of uncertainty. @friedman1957 proposed a simple formulation that remains an excellent description of annual income shocks even today. Friedman said that there are two components to income: A 'permanent' component that is roughly what they would expect to earn in a 'normal' year (say, their annual salary), and a 'transitory' component that reflects events like unemployment spells or lottery winnings; these make a given year's realized income deviate from its expected value.

To meld Friedmanian uncertainty with a Modlglianian life cycle, we need one more definition, whose purpose is to capture the predictable patterns that (noncapital) income follows over the lifetime (income starts low, rises with age and experience, and falls at retirement to the level of any regular pension payments):
\begin{align}
    \permGroFac_{t+1} & : \text{typical life cycle permanent income growth factor by age}
\end{align}

The typical life cycle pattern is altered, in any particular consumer's case, by 'permanent shocks' which we represent with the variable $\permShk$. At any given age, permanent growth can deviate from the average experience of others of the same age in either a positive direction ($\psi>1$ would correspond to an unexpected promotion or a switch to a higher-paying job) or a negative direction ($\psi < 1$ might be the result of a failure to be promoted or a change to a lower paying job).

This gives us the following description of the dynamics of permanent income $\pLvl$:
\begin{align}
    \pLvl_{t+1} & = \pLvl_{t} \permGroFac_{t+1} \permShk_{t+1}
    \\ \Ex_{t}[\pLvl_{t+1}] & = \pLvl_{t} \permGroFac_{t+1}
\end{align}
where the second line follows from the first because the expected value of the permanent shock is $\Ex_{t}[\permShk]=1$.

The transitory shock to income has two modes. In unemployment spells, the consumer earns no income; we assume that such spells occur with probability $\pZero$.If the consumer remains employed, we will assume that the income shocks are lognormally distributed:[^betterunemp]
\begin{align}
    \tranShkEmp_{s} = &
    \begin{cases}
        0\phantom{/\pZero} & \text{with probability $\pZero>0$}
        \\ \xi_{s}/\pZero & \text{with probability $(1-\pZero)$}
    \end{cases}
\end{align}

[^betterunemp]: It is straightforward to extend the model to allow for a more realistic treatment of unemployment, for example by taking account of the existence of an unemployment insurance system; such an adjustment does not change the substantive conclusions we are interested in.

It is conventional to assume that shocks to permanent income and to the transitory income of the employed are lognormally distributed:
\begin{align}
    \log \permShk_{s} \thicksim \mathcal{N}(-\sigma_{[\permShk, t]}^{2}/2,\sigma_{[\permShk, t]}^{2})
    \\ \log \xi_{s}\thicksim \mathcal{N}(-\sigma_{[\xi, t]}^{2}/2,\sigma_{[\xi, t]}^{2})
\end{align}
which, together with the other assumptions, guarantee that the expected value of the transitory and of the permanent shocks are both 1: $\Ex_{t}[\permShk_{t+1}]=\Ex_{t}[\tranShk_{t+1}]=1$. (We use standard calibrations of both of these shock processes.)

Under the assumptions we have made about the structure of the utility function (homotheticity) and budget constraint (linearity and geometric returns), it is possible to recast the problem entirely in terms of _ratios_ of the model variables to permanent income $\pLvl$. So, for example, italic $\cNrm = \cLvl/\pLvl$ is the ratio of the (boldface) level of consumption to the level of permanent income $\pLvl$ (see @BufferStockTheory for the math).

Another way to make the problem easier to understand is to combine several of the multiplicative terms into portmanteau variables. Defining boldface $\pmb{\DiscFac}_{t+1}$ as
\begin{align}
     \pmb{\DiscFac}_{t+1} & ={\beta} (\permShk_{t+1} \permGroFac_{t+1})^{1-\CRRA}
    %\\ \RNrm_{t+1} & = \left(\frac{\Rfree}{\permShk_{t+1}\permGroFac_{t+1}}\right)
\end{align}

%and simplifying the notation for the probability of survival to $\Alive_{t+1} \equiv \Alive_{t}^{t+1}$

Under the assumptions we have made, it turns out that the consumer's problem can be expressed more simply by realizing that it boils down to a 'now versus later' problem.  All the consumer needs to know about the future is summarized by the value they will expect as a consequence of ending the current period with a certain ratio of assets to permanent income, $\aNrm = \aLvl/\pLvl$. We can represent the value of ending the period with assets of $\aNrm$ using the Gothic variant of the letter $\vFunc$:
\begin{align}
    \mathfrak{v}_{t}(\aNrm_{t}) & = \Ex_{t}[\pmb{\DiscFac}_{t+1}\vFunc_{t+1}(\mNrm_{t+1})]
\end{align}

Finally we are ready to add portfolio choice to the problem. Suppose the consumer can invest in a risky asset that earns rate of return $\log \Risky \thicksim \mathcal{N}(\rfree + \eprem - \sigma^{2}/2, \sigma^{2})$. That is, we make the conventional assumption that the risky asset is distributed lognormally with an expected equity premium of $\eprem$.

The portfolio return the consumer earns will depend on the share of their assets they invest in the risky versus the safe asset. Calling the share $\varsigma$, the portfolio-weighted rate of return will be
\begin{align}
    \Rport_{t+1} & = \Rfree + (\Risky_{t+1}-\Rfree)\varsigma
\end{align}
and the consumer is assumed to make the optimal choice of portfolio share:
\begin{align}
\mathfrak{v}_{t}(a) & = \max_{\varsigma}~~ \Ex_{t}[\pmb{\beta}_{t+1} \vFunc_{t+1}(\Rport_{t+1} a + \theta_{t+1})
\end{align}

The consumer's objective in the consumption stage of the problem can be expressed in Bellman form as:
\begin{align}
    {\vFunc}_{t}({\mNrm}_{t}) & = \max_{\{\cNrm_{t}\}} ~ \uFunc(\cNrm_{t})+\Alive_{t+1} \mathfrak{v}_{t}(\aNrm_{t})
    \\ & \text{s.t.} &
    \\ \aNrm_{t} & = {\mNrm}_{t}-\cNrm_{t}
    % \\ {\mNrm}_{t+1} & = \aNrm_{t}\RNrm_{t+1} + ~\tranShkEmp_{t+1}
\end{align}

<br>

| object                                 | meaning                                                                                 |
| -------------------------------------- |                      ------------------------------------------------------------------ | 
| $\mNrm, \cNrm, \aNrm$                  | market resources, consumption, and end-of-period assets, normalized by permanent income |
| $\vFunc$                               | the normalized value function                                                           |
| $\Alive_{t+1} \equiv \Alive_{t}^{t+1}$ | probability a person alive at date $t$ survives to date $t+1$                           |

<br>

{and} since $\aNrm$ measures available market resources that are unspent, this formulation makes it crystal clear that the consumer faces a tradeoff between the utility of consumption today and the expected value of preserving assets $\aNrm=\mNrm-\cNrm$ for the future.[^normalization]

[^normalization]: The normalization for value function involves more than just division by $\pLvl$; see @BufferStockTheory for details.

We calibrate the model to include two kinds of uncertainty after retirement.

First, we incorporate estimates from @velasquezgiraldoJMP of the size of shocks to medical expenditures for retirees; a perfectly rational reason not to run down your wealth, or not to run it down too far, is a fear of large medical expenses that you want to be able to meet.  Such uncertainty has the potential to deter the drawdown of wealth; see @ameriks2011joy for an argument that it is the principal explanation for the 'drawdown failure.'  While such effects are present in our model, our model estimation results below will find that the model still predicts much more drawdown of wealth than the data show.

Second, we assume that there are 'ordinary' expenditure shocks in retirement that are of similar magnitude to income shocks during working life (following recent estimates from  @flExpShocks).  Again, in principle, the presence of such shocks provides a precautionary motive to draw down wealth more slowly.

### The LCP model with 'Warm Glow' Bequests

The LCP model sketched above assumes that the only reason to hold wealth is to spend it later -- which means that eventually an age must come at which the wealth starts being spent down. As the literature has demonstrated, and as we will confirm below using data from SCF's from 1995 to 2022, the path of the median wealth ratio after retirement does not look anything like what that model predicts. 

[^selection]: The profile in the data is undoubtedly subject to a selection effect caused by the fact that people who are richer tend to live longer. But the adjustments required to take that into account are small and do not modify this conclusion.

Of course, the model can make no sense at all of the behavior of the very rich. Bill Gates, for example, has chosen to allocate a large portion of his lifetime wealth to the Bill and Melinda Gates foundation rather than spending it on himself; and even with the pittance that remains to him (\$153 billion, according to [Business Insider](https://www.businessinsider.com/how-bill-gates-spends-fortune)) he would need to spend about \$22 million a day to *avoid getting richer*.[^billgatesspend]  (In fact, he has pledged to give away nearly all of his wealth before he dies).

[^billgatesspend]: As of 2024-05-15, the Fed Funds rate is 5.3 percent at an annual rate. \$153b $\times$ 0.053/365 days $\approx$ \$22 million. At the current inflation rate of 3.4 percent, he would only have to spend a little over \$8 million a day to run down his real wealth -- assuming the Fed Funds rate is the highest rate of return he can earn.

But the model also fails for people of much more modest means.  For a substantial fraction of normal retirees, the drawdown phase seems never to come (the 'drawdown failure' mentioned in the introduction).

From the mathematical point of view, it is clear that some other motive for holding onto wealth must be added to the framework if it is to explain these facts (never mind Bill Gates). A natural candidate is a bequest motive: The idea that people take pleasure in the thought of leaving something to their heirs.

This can be accommodated simply by adding another term to the sources of utility: the value the consumer places on the bequest, which we will denote as $\bqstNrm(\aNrm)$ (think of this as the utility they experience from the thought of leaving an $\bqstNrm$state).

Defining the probability of passing away as the probability of not $\Alive$iving to the next period,
\begin{align}
    \cancel{\Alive} & =(1-\Alive)
\end{align}
the flow of utility that the consumer receives includes both their utility from consumption _and_ the pleasure they take from the thought that, if they pass away before next period (which happens with probability $\cancel{\Alive}$), their assets will pass to their heirs.

The consumer's new value function is therefore just
\begin{align}
    {\vFunc}_{t}({\mNrm}_{t}) & = \max_{\cNrm_{t}} ~ \overbrace{\uFunc(\cNrm_{t})}^{\text{present}}+\overbrace{\underbrace{\Alive_{t+1}\mathfrak{v}(\aNrm_{t})}_{\text{live}} + \underbrace{\cancel{\Alive}_{t+1}\bqstNrm({\aNrm}_{t})}_{\text{die}}
    }^{\text{future}}.
\end{align}

The literature has commonly used a `warm glow utility from bequests' motive of the form:
\begin{align}
    \bqstNrm(a) & = \alpha\frac{(a+\underline{a})^{1-\CRRA}}{1-\CRRA}
\end{align}
where the $\CRRA$ coefficient is the same as in the utility function for consumption (see, e.g., @deNardiBequest), and the $\alpha$ coefficient controls the importance of the bequest motive relative to the utility from consumption.

## Wealth in the Utility Function

Our estimation below will find little evidence that a bequest motive of this kind is important for the median college-educated retiree. It also seems unlikely to be important for much richer people, at least according to the evidence from the historian Fredrick Cople @jaherGilded's chronicle of the behavior of the richest Americans since the Revolution. Jaher presents a feast of quotations articulating a host of motivations for extreme wealth accumulation; but among their many explanations of their behavior, almost none of the tycoons under study mention anything resembling the bequest motive as formulated in the standard academic life cycle literature. (Andrew Carnegie was most explicit: 'I would rather leave my son a curse than the almighty dollar.')[^carnegie]  This is one of those places where economists' new openness to the idea of taking seriously what people say about their motivations has bite. While it is not unreasonable to be sceptical about taking such quotations at face value, @WhyDoTheRich shows that essentially all of the motivations articulated (wealth brings power; wealth allows philanthropy; wealth is a way of 'keeping score'; and more) can be captured in a mathematical formulation in which wealth enters the utility function directly.

[^carnegie]: He made good on this: He gave away more than 90 percent of his wealth before he died, to the astonishment of many skeptics.

As mentioned above, the [Survey of Consumer Finances](https://doi.org/10.17016/8799) has for many years asked respondents a question about their motivations for saving.[^whysave] While respondents' answers are fairly heterogeneous, the SCF has a suggested aggregation of the many different answers into categories that correspond approximately to some of the motivations that the academic literature has considered.  The category that best matches the 'bequest' motivation is 'Family' (which includes 'to help the kids out' and 'to leave an estate' but also includes saving for 'weddings and other cermonies' and  'to have children/a family.')

[^whysave]: See the material starting at line 848 in [the documentation]((https://www.federalreserve.gov/econres/files/bulletin.macro.txt).

An ambitious agenda would be to tabulate the answers to this survey question for people at different ages and then to construct a model that would imply the same age pattern of motivations as the data.  For example, one might find that for people who have just entered the labor market (say, the 26-30 age group) the survey responses showed that saving for 'retirement' was not a priority, while saving for 'purchases' and 'liquidity' were important. In order for a model to be credible, its implications would need to comport with the survey data.
 
 Our aim here is to take a first step in that direction, by constructing a model that is at least consistent with the responses of retirees.

(most-important-reason)=
### Table: Most Important Reason for Saving 
The table below presents the responses to this question for college-educated households older than age 70 from the 1995 to the 2022 waves of the SCF:

<br>

 | Reason | Proportion | Explanation |
 | --- | --- | --- | 
 | 'Family' | 0.06 | Bequests; weddings, etc |
 | 'Retirement' | 0.27 |  | 
 | 'Liquidity/The Future' | 0.40 | | 
 | 'Purchases'  | 0.13 | cars, vacation homes, etc | 
 | 'Cannot save' | 0.06 | |
 | Other | 0.08 | | 

<br>

If bequests were a primary motivation for saving for most (college-educated) people, it would be surprising for them to mention this motivation so rarely.

Given these (and other) objections to the bequest motive, and given the problems of the model without a bequest motive, it seems natural to consider alternative modifications to the framework.

### Technical Details (functional form)

The most general way we economists have of incorporating people's motivations into our models of behavior is simply to assume that the decisionmaker directly values something -- in this case, wealth. The next question is how best to incorporate the item in the utility function to study any particular question.  @WhyDoTheRich, for example, proposed a utility function specifically designed to capture saving behavior as wealth approached infinity, and accomplishing that goal required some mathematical structure that delivered the desired results but was unwieldy (and not obviously necessary for explaining the behavior of the bottom 99 percent, whose wealth does not approach infinity).[^richutility]

[^richutility]: Specifically, a separable utility-from-wealth function was added to the maximizer's objective and with a coefficient of relative risk aversion smaller than that for the utility from consumption.

*Money in the Utility Function* 

It turns out that there is a literature in macroeconomics, pioneered by Miguel @sidrauski1967rational, that has long included 'money' in the utility function of the representative agent in one form or another.

A well-known paper by [](doi:10.1086/261207) proposed a specific utility function designed to capture the stability of the ratio of money to GDP, and Rotemberg along with James Poterba estimated this model on U.S. data in [](doi:10.3386/w1796).

The structure of their utility function is
\begin{align}
    \uFunc(\cNrm,\lqdt) & = \frac{\left(
        \cNrm^{1-\delta}\lqdt^{\delta}
        \right)^{1-\CRRA}}{1-\CRRA}
\end{align}
where $\lqdt$ captures the the $\lqdt$iquidity services provided by money-holding.  

To be clear, the aim of that literature was to explain the holding of $\lqdt$ defined as dollar cash holdings, to study questions like the 'velocity' of money and the role of money supply and money demand in determining interest rates -- not to explain saving behavior.  

*Wealth In the Utility Function: Cobb-Douglas Form*

But for the question of how to incorporate wealth in the utility function, [](doi:10.2139/ssrn.4693176) proposed a mathematically identical formulation,
\begin{align}
    \uFunc(\cNrm,\aNrm) & = \frac{\left(
        \cNrm^{1-\delta}\aNrm^{\delta}
        \right)^{1-\CRRA}}{1-\CRRA}
\end{align}
where $\aNrm$ takes the place of $\lqdt$ in the Rotemberg-Poterba utility function.[^mora] The Cobb-Douglas functional form for the TRP utility function is commonly used in other contexts, but does not seem to have been explored as a formulation for how to put a direct wealth-holding motive in the utility function.

[^mora]: The question of whether $\aNrm$ or $\mNrm$ should be in the utility function is of little importance; here we prefer $\aNrm$ because assets after consumption are immune to considerations of whether the time period is a year, a quarter, a month, or a day.

The upshot is that if we credit the proposition that the ownership of wealth yields utility, then there is good precedent for the functional form of [](doi:10.2139/ssrn.4693176).
% AL: Add citation to the 1998 paper you found
Henceforth we will call this the Tzitzouris-Rotemberg-Poterba or 'TRP' utility function.

It is a simple matter to solve the revised problem with wealth in the utility function using the TRP utility specification. The revised value function of the problem is:
\begin{align}
    {\vFunc}_{t}({\mNrm}_{t}) & = \max_{\cNrm_{t}} ~ \uFunc(\cNrm_{t}, \aNrm_{t})+\Alive_{t+1}\mathfrak{v}_{t}(a_{t})
\end{align}

We refrain from a description of the methods of solution here because they are documented in the accompanying code archive which fully reproduces all our results.

(We are open to the possibility that wealth in the utility function is a reduced form for other motivations -- indeed, that was the thesis of @WhyDoTheRich.  In particular, the fact that in our SCF table above, 'Liquidity/The Future' is the most popular answer among retirees for the most important reason to save might signal that the forms of uncertainty that we can measure -- like the @Ameriks2020jpe calculations about nursing home expense risks -- constitute only a fraction of the matters retirees might worry about.  Maintaining a buffer stock of wealth to protect oneself against 'unknown unknowns' is possibly perfectly rational, and also nearly impossible to calibrate in a quantitative model in which we would need to have an accurate representation of people's beliefs about the magnitude, frequency, and persistence of 'unknown unknowns.'  But if you knew those answers, they would be, at best, 'known unknowns.')


# Estimation

### Indirect Inference Described

Even if you knew all the parameters of the model (the consumer's coefficient of relative risk aversion, etc), solving an optimization problem that includes the many real-world complications described above (especially those due to uncertainty) is such a formidable problem that it only became possible about 25 years ago (and solving the models took days).

But of course we do not know the best values to choose for unobservable parameters like relative risk aversion and time preference rates. The solution to this problem that is becoming standard is the method of 'indirect inference.' Essentially, this means specifying the structure of your model except for the values of parameters that you cannot measure well (like time preference and risk aversion), and asking a numerical search algorithm to seek the values of those parameters that lets the model fit the data as well as it is capable of doing. This requires the computer to solve the problem perhaps thousands of times, which is why indirect inference has only begun to come into its own recently - as computer speeds have gotten fast enough to tackle the problem.

### Indirect Inference Implemented

We are particularly interested in finding the optimal post-retirement choices, both for the rate of spending and for portfolio allocation between safe and risky assets.


*The Method of Simulated Moments*

The method of simulated moments consists of finding the parameters that make the model's simulated moments (statistics), like the median wealth and the median portfolio share, match the corresponding empirical facts as closely as possible.

Consider a real moment $y_i$ where $i \in [1, N]$ and the corresponding simulated moment $\hat{y}_i(\theta)$, where $\theta$ is the vector of parameters that we are interested in estimating. By solving and simulating our structural model with different $\theta$ parameters, we can calculate the simulated moments $\hat{y}_i(\theta)$ for each parameter set. The method of simulated moments then consists of finding the parameter set $\theta$ that minimizes the distance between the simulated moments and the real moments. This is done by minimizing the following objective function:

\begin{equation}
    \min_{\theta} \sum_{i=1}^{N}  \left( \omega_i [y_i - \hat{y}_i(\theta) ] \right)^2
\end{equation}

where $\omega_i$ is the weight of each moment in the objective function, representing the relative importance of each moment in the estimation process. For example, we might be more interested in matching the median wealth than the median portfolio share, so we would assign a higher weight to the former.

For our exercise, we are interested in matching the median wealth to income ratios throughout the life-cycle, and the median portfolio share of risky assets after retirement. Because aggregate age data can be noisy and subject to selection bias and measurement error, we will aggregate the data into 5-year age bins to smooth out the noise and reduce the impact of selection bias. Starting at age 25, we calculate the median wealth to income ratio as follows: Wealth is defined as the sum of all assets and liabilities, including financial assets, housing, vehicles, and debt. For income, we use the sum of all wages, salaries, social security, and retirement income, excluding capital gains and other non-recurring income. We then calculate the wealth to income ratio of every household in the age bin and remove households with an income of zero. The median wealth to income ratio is calculated from the remaining households. An important point is that in our structural model we hard-code retirement at age 65, whereas in the data we observe retirement at different ages, but predominantly between ages 60 and 70. Therefore, we avoid the data for ages 60 to 70 to prevent any bias in the estimation process, but keep the data for ages 70 and above to capture the behavior of retirees. Similarly, we calculate the median portfolio share of risky assets after retirement for ages 70 and above given by @Aboagye2024.

Considering the selection of moments we have chosen, it is clear that there is an inbalance between the wealth to income moments and the portfolio share moments. There are more wealth to income moments than portfolio share moments, (12 to 5), and the portfolio share moments lie between 0 and 1, whereas the wealth to income ratios can be much larger. To account for this, we set the weights to normalize the wealth to income ratios by the highest ratio in the data, making them all lie between 0 and 1, and set the weights for the portfolio share moments to multiply by 12/5, so that the two sets of moments are equally weighted in the estimation process. This ensures that our estimation process puts even weight on the two sets of moments, despite the difference in scale and number of moments.

Having pinned down the moments we are interested in matching and their respective weights, we can now proceed to a discussion of estimating the parameters of our vaious models. We use the `Econ-ARK` project's `HARK` package to solve and estimate the models, and `estimagic` (@Gabler2022) to perform the estimation process. Our exercise consists of estimating 1 parameter (the constant coefficient of relative risk aversion (CRRA) parameter for the Life Cycle Portfolio Choice Model) up to 3 parameters (CRRA, the weight of the bequest motive, and the wealth-shifter of utility parameter for the `LCP+WarmGlow` model), so we develop a robust and efficient estimation process that can handle a varying number of parameters. <!-- % We call the merging of features from the `HARK` and `estimagic` packages `Estim-ARK`.-->

Our estimation process is computationally expensive, requiring the solving and simulation of the model given a parameter set many times. Because our simulated moments indeed require simulation, our moment generating functions $\hat{y}_i(\theta)$ have no analytical derivatives with respect to the parameters, so we must rely on numerical differentiation and clever optimization algorithms to find the optimal parameter set. We use the `tranquilo` algorithm (@Gabler2024), which stands for TrustRegion Adaptive Noise robust QuadratIc or Linear approximation Optimizer, to find the optimal parameter set. The `tranquilo` optimizer has many attractive features, such as being able to evaluate the function in parallel and estimate even noisy objective functions with many parameters, as well as being especially designed for least squares problems, such as the MSM.

### Indirect Inference Results

```{include} results.md
```

# Conclusion

To thoughtful academics, it has long been disturbing that the financial advice industry has paid so little attention to our hard work in constructing and solving impressively sophisticated dynamic stochastic optimization models of financial behavior. Those of us with a bit of humility have always suspected that the failure has been on our side: If all we could offer was models that produced risible advice like 'everyone should spend down their wealth to zero and live pension-check to pension-check,' while financial analysts' real world experience told them that such advice would get them fired, then it was reasonable to disregard the academic literature.

The thesis of this paper, though, is that a confluence of factors has now finally brought us to a point where state-of-the-art mathematical/computational optimization models can provide advice that makes sense, when the model assumptions are also disciplined by survey data and the tacit knowledge of financial advisors.[^housing]

[^housing]: Much more remains to be done to improve the models further; for example, a question of great practical importance that is now just at the edge of possibility of being computationally solved is to calculate the implications of nonfinancial (principally, housing) wealth for optimal financial choice. Because homeownership is such a complex phenomenon, the academic literature is only now reaching the point at which it may be possible to answer questions like "if I own a house, how should I modify my spending and portfolio plans to take that into account?" We do know the *direction* of the effect. @kimballStandardRA shows that the addition of a new uncontrollable risk reduces the optimal choice of exposure to controllable risks like the stock market. But *by how much* one's stock exposure should be reduced because of house-price risk can only be answererd by solving a quantitatively plausible model.

It would be a better world if financial advice could be justified as reflecting the mathematically optimal solution to a well-defined problem.  Not only would academics have the satisfaction of knowing that they had finally come close to fulfilling the vision of Modligliani and Brumberg 70 years ago. Financial analysts could also sleep more soundly in the knowledge that the advice they were giving were what many people probably think it already is: The adaptation to the client's particular circumstances of the advice that is the best that can be delivered by the latest high-tech computational optimization tools.

The time seems ripe for a much closer collaboration between academia and the financial industry in building this better world.  This paper's open-source code, built with the associated open-source [Econ-ARK](https://econ-ark.org) project's tools, would be a good place to start.[^thankstrp]

[^thankstrp]: We are grateful to the Sloan Foundation and to T Rowe Price for generous funding of the toolkit.




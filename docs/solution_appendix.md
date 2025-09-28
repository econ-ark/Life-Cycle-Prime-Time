# Appendix: Solution Methods

In this appendix, we provide additional details for how the intertemporal optimization problems in our life-cycle models are solved. The method for finding consumption in the basic life-cycle and warm-glow bequest models is taken directly from @CarrollEGM, and the method for finding optimal portfolio shares (in all models) uses standard techniques. The wealth-in-utility model has a novel solution method.


## Optimal Portfolio Share

Each of our models has two continuous control variables-- consumption $\cNrm_t$ and the risky asset share $\varsigma_t$-- that are chosen simultaneously, but we solve them as if they are chosen sequentially. The agent's state variable when they choose $\varsigma_t$ is thus their assets after buying consumption, $\aNrm_t = \mNrm_t - \cNrm_t$. The agent's problem at this point is:

\begin{align}
\mathfrak{v}_{t}(\aNrm_t) & = \max_{\varsigma \in [0,1]}~~ \Ex_{t}\left[ \pmb{\beta}_{t+1} \vFunc_{t+1}(\Rport_{t+1} \aNrm_t + \theta_{t+1}) \right] ~~ \text{s.t.} ~~ \Rport_{t+1} = \Rfree + (\Risky_{t+1 }-\Rfree)\varsigma.
\end{align}

Note that the survival probability $\Alive_{t+1}$ is *not* included in this problem because it is a constant scaling factor that cannot affect the optimal choice of $\varsigma_t$. Likewise, the warm-glow bequest motive $e(\aNrm_t)$ is also irrelevant because it is constant with respect to $\varsigma$.

We will not reproduce the proof here, but it can be shown that the first order condition is necessary and sufficient to characterize the optimal risky portfolio share as long as $\vFunc_{t+1}$ is strictly concave (which can also be proven). Taking the derivative of the maximand with respect to $\varsigma$ and equating it to zero yields:

\begin{equation}\label{eq:foc-share}
\Ex_{t}\left[ \pmb{\beta}_{t+1} (\Risky_{t+1}-\Rfree) \aNrm_t \vFunc'_{t+1}((\Rfree + (\Risky_{t+1}-\Rfree)\varsigma) \aNrm_t + \theta_{t+1}) \right] = 0.
\end{equation}

The left-hand side is monotone in $\varsigma$ and thus the FOC has at most one interior solution. The constraint that the consumer cannot short the risky asset ($\varsigma \geq 0$) is never binding as long as mean risky return exceeds the risk-free return. However, the constraint that they cannot short the risk-free asset to buy even more of the risky asset ($\varsigma \leq 1$) *does* sometimes bind. Our algorithm for find the optimal $\varsigma$ is as follows:

1. Fix an exogenous grid of $\aNrm_t$ values from $0$ to a large value (say, a wealth-to-income ratio of 100).

2. For each $\aNrm$ in that grid, evaluate the left-hand side of the FOC above. If it is less than or equal to zero, then $\varsigma = 1$ for that gridpoint. Otherwise, continue.

3. Solve the FOC for $\varsigma$ using a standard numeric rootfinder (e.g., Brent's method), bounded above by 1 and below by the Samuelson risky asset share.

@Samuelson1969 characterized the optimal risky asset share in the absence of labor income risk, which is also the lower limit of the risky asset share as $\aNrm$ becomes arbitrarily large (and thus labor income risk becomes increasingly irrelevant). This value can thus be used both to bound the search for an interior solution to the FOC, and in the extrapolation of the risky share policy function above the top gridpoint. Specifically, we construct the policy function as a linear interpolant over the $(\aNrm, \varsigma)$ gridpoints with an exponential decay extrapolation to the Samuelson limit above the top gridpoint.

As discussed further below, marginal value $\vFunc'_{t+1}(\mNrm_{t+1})$ in all of our models is simply equal to the marginal utility of consumption at that value of market resources. Hence we never need to represent the value function itself, as the consumption function in $t+1$ (and preference parameters) carries all information needed to make optimal choices in period $t$.


## Optimal Consumption in Baseline and Warm-Glow Bequest Models

Stepping back within the period, we can now consider the choice of optimal consumption, taking as given that the agent will optimally allocate their assets between the risky and risk-free assets. For our first two models, we express the *continuation value* over $\aNrm_t$ as:

\begin{equation}
\bar{\mathfrak{v}}_t(\aNrm_t) = \begin{cases}
\Alive_{t+1} \mathfrak{v}_t(\aNrm_t) & \text{in baseline life-cycle model} \\
\Alive_{t+1} \mathfrak{v}_t(\aNrm_t) + (1 - \Alive_{t+1})e(\aNrm_t) & \text{in warm-glow bequest model} \\
\end{cases}.
\end{equation}

The optimization problem in the consumption-choice step can then be written as simply:

\begin{align}
\vFunc_t(\mNrm_t) &= \max_{\cNrm} \left[ \frac{\cNrm^{1-\CRRA}}{1 - \CRRA} + \bar{\mathfrak{v}}_t(\mNrm_t - \cNrm) \right].
\end{align}

This has a first order condition that is necessary and sufficient to characterize optimal consumption:
\begin{equation}\label{eq:EGM-FOC}
\cNrm_t^{-\CRRA} - \bar{\mathfrak{v}}'_t(\mNrm_t - \cNrm_t) = 0 \Longrightarrow \cNrm_t = \bar{\mathfrak{v}}'_t(\aNrm_t)^{-1/\CRRA}.
\end{equation}

The algorithm for solving for optimal consumption is thus:

1. Fix an exogenous grid of $\aNrm_t$ values from $0$ to a large value (say, a wealth-to-income ratio of 100); this can be the same or a different grid from above.

2. For each $\aNrm$ in the grid, evaluate the right-hand side of @eq:EGM-FOC, yielding the $\cNrm_t$ consistent with this level of end-of-period assets.

3. Find the associated decision-time state by inverting the intraperiod budget: $\mNrm_t = \aNrm_t + \cNrm_t$.

4. Construct the consumption function as a linear interpolant over those $(\mNrm_t, \cNrm_t)$ pairs, adding a point at $(0,0)$ to incorporate the liquidity-constrained portion of the consumption function.

5. Construct the marginal value function $\vFunc'_t(\mNrm_t)$ as the composition of the marginal utility function and the consumption function.

In the final step, we apply the standard envelope condition logic, which says that the marginal value of holding just a bit more market resources is equal to the marginal utility of consuming a tiny bit more (relative to the optimal level). This is obvious when the consumer is liquidity constrained: if they had a bit more cash-on-hand, they would consume that marginal dollar, yielding the marginal utility of consumption and *still* end the period with no assets. When the consumer is not constrained, the first order condition for optimal consumption means that they were indifferent to the allocation of the last bit of resources between consumption and saving. Hence the marginal value of a bit more market resources equals both the marginal continuation value *and* the marginal utility of consumption.


## Optimal Consumption in the Wealth-in-Utility Model

With a standard CRRA utility function over consumption, marginal utility of consumption is very simple expression, and so the first order condition for optimal consumption was trivial to solve, as in @eq:EGM-FOC. With the alternate preferences in the Wealth-in-Utility model, this is not the case. Recall that utility in this model involves a Cobb-Douglas aggregation of consumption $\cNrm_t$ and assets $\aNrm_t$ inside of a CRRA function:

\begin{align}
    \uFunc(\cNrm, \aNrm) & = \frac{\left(\cNrm^{1-\delta}\aNrm^{\delta}\right)^{1-\CRRA}}{1-\CRRA} = \frac{\left(\cNrm^{1-\delta}(\mNrm - \cNrm)^{\delta}\right)^{1-\CRRA}}{1-\CRRA}.
\end{align}

Fixing market resources $\mNrm_t$ at some value of interest, the marginal return to utility from consumption is:

\begin{align}
\frac{\text{d}}{\text{d} \cNrm} \uFunc(\cNrm, \mNrm-\cNrm) &= \left[ (1-\delta) \cNrm^{-\delta} (\mNrm - \cNrm)^\delta - \delta \cNrm^{1-\delta}(\mNrm - \cNrm)^{\delta-1} \right] \cdot \left( (\mNrm - \cNrm)^\delta \cNrm^{1-\delta}  \right)^{-\CRRA} \\
 &= \left[ (1-\delta) \left(\frac{\cNrm}{\mNrm-\cNrm}\right)^{-\delta} - \delta \left(\frac{\cNrm}{\mNrm - \cNrm} \right)^{1-\delta} \right] \cdot \left( (\mNrm - \cNrm)^\delta \cNrm^{1-\delta}  \right)^{-\CRRA} \\
 &= \left[ (1-\delta) \left(\frac{\cNrm}{\aNrm}\right)^{-\delta} - \delta \left(\frac{\cNrm}{\aNrm} \right)^{1-\delta} \right] \cdot \left( \aNrm \aNrm^{\delta-1} \cNrm^{1-\delta}  \right)^{-\CRRA} \\
 &= \left[ (1-\delta) \chi^{-\delta} - \delta \chi^{1-\delta} \right] \cdot \left( \aNrm \chi^{1-\delta}  \right)^{-\CRRA}, ~~~~ \chi \equiv (\cNrm/\aNrm).
\end{align}

These algebraic manipulations will prove useful when we solve the first order condition momentarily. With wealth-in-utility preferences, the agent's optimal consumption problem is:

\begin{align}
\vFunc_t(\mNrm_t) &= \max_\cNrm \left[ \frac{\left(\cNrm^{1-\delta}(\mNrm_t - \cNrm)^{\delta}\right)^{1-\CRRA}}{1-\CRRA} + \bar{\mathfrak{v}}_t(\mNrm_t - \cNrm) \right].
\end{align}

Consider the first order condition for optimality by taking the derivative of the maximand with respect to $\cNrm$ and equating it to zero:

\begin{equation}
\frac{\text{d}}{\text{d} \cNrm} \uFunc(\cNrm_t, \mNrm_t-\cNrm_t) - \bar{\mathfrak{v}}'_t(\mNrm_t - \cNrm_t) = 0.
\end{equation}

We can substitute the final form of the marginal return to consumption, move the second term to the right-hand side, and then rearrange slightly to get:

```{math}
:label: eq:FOC-WIU

\begin{align}
\left[ (1-\delta) \chi_t^{-\delta} - \delta \chi_t^{1-\delta} \right] \cdot \left( \aNrm_t \chi_t^{1-\delta}  \right)^{-\CRRA} &= \bar{\mathfrak{v}}'_t(\aNrm_t) \\
\left[ (1-\delta) \chi_t^{-\delta} - \delta \chi_t^{1-\delta} \right]^{-1/\CRRA} \cdot \chi_t^{1-\delta}  &= \underbrace{\bar{\mathfrak{v}}'_t(\aNrm_t)^{-1/\CRRA} / \aNrm_t}_{\equiv ~ \omega_t}.
\end{align}
```

Note that the left-hand side of the rearranged FOC is monotonically increasing with respect to $\chi = \cNrm/\aNrm > 0$, starting from zero and growing without bound. Moreover, the RHS (which uses *only* information about the continuation value through $\aNrm_t$) must be strictly positive, as both marginal value and end-of-period assets are strictly positive (the consumer will never choose $\aNrm=0$ with these preferences because it would yield infinitely negative utility). Hence the first order condition has a unique solution in $\chi_t$ for each $\aNrm_t$. 

Unlike with basic CRRA utility, there is no closed form solution for @eq:FOC-WIU to recover $\chi_t$ from $\omega_t$. While it would be possible to use a rootfinder to solve @eq:FOC-WIU for each value of $\omega_t$ as it comes up during the solution process, it is more efficient to pre-compute a function that accurately maps from $\omega$ to $\chi$. We now describe a method for constructing such a function by working with the inverse relationship.

First, note that the expression in square brackets is not positive for all values of $\chi > 0$, with the bounding condition defined by:

\begin{equation}
(1-\delta) \chi^{-\delta} - \delta \chi^{1-\delta} \gt 0 \Longrightarrow (1-\delta) \chi^{-\delta} \gt \delta \chi^{1-\delta} \Longrightarrow \frac{1-\delta}{\delta} \gt \chi.
\end{equation}

The expression in square brackets is raised to a negative power, which would yield a complex result with a negative input, hence we need only to consider values of $\chi \in (0, (1-\delta)/\delta)$. These $\chi$ values represent the *range* of the function that maps from $\omega$ to $\chi$, and we want our constructed approximation to cover as much of that range as possible. To do so, we will use the logit transformation to map from an auxiliary variable $z \in \R$ to $\chi \in (0, (1-\delta)/\delta)$:

\begin{equation}\label{eq:zToChi}
\chi = \frac{\exp(z)}{1 + \exp(z)} \cdot \frac{1-\delta}{\delta}.
\end{equation}

The domain of the function we want to approximate is $\omega > 0$ or $\omega \in \R_+$, so we can work with $\log(\omega)$ to ensure that we are working with strictly positive numbers. To make our approximate mapping from $\omega$ to $\chi$, we do the following:

1. Fix a grid of $z$ values centered around zero; we use a uniformly spaced grid with 301 gridpoints between $\pm 15$.

2. For each $z$ in the grid, calculate the corresponding $\chi$ using @eq:zToChi. With our $z$ grid, this spans the inner 99.99994\% of the feasible range of $\chi$.

3. For each $\chi$ in that grid, calculate $\omega$ using @eq:FOC-WIU, then compute $\log(\omega)$.

4. Construct a linear spline interpolant that maps from the vector of $\log(\omega)$ values to the grid of $z$, with linear extrapolation above and below; call this function $g(\cdot)$.

5. Define function $f(\cdot)$ as the composition of @eq:zToChi, $g$, and $\log$.

By construction, $f$ is an approximation of the mapping from $\omega$ to $\chi$ implicitly defined by @eq:FOC-WIU, by successively applying the logarithm to $\omega$, the interpolant from $\log(\omega)$ to $z$, and the logit transformation to recover $\chi$. The approximation is extremely accurate, even on the extrapolated region on $\omega$, because the underlying mapping from $\log(\omega)$ to $z$ approaches linearity on both ends. Conveniently, the $f$ function depends on only $\CRRA$ and $\delta$ and can be constructed once for all periods of the life-cycle.

With the mapping $f : \omega \rightarrow \chi$ in hand, we can now describe our algorithm for solving for optimal consumption under wealth-in-utility preferences:

1. Fix an exogenous grid of $\aNrm_t$ values from $0$ to a large value (say, a wealth-to-income ratio of 100); this can be the same or a different grid from above.

2. For each $\aNrm$ in the grid, evaluate $\bar{\mathfrak{v}}'_t(\aNrm_t)$, then raise it to the $-1/\CRRA$ power and divide by $\aNrm$, yielding a vector of $\omega$ values.

3. For each $\omega$ in that vector, compute $\chi = f(\omega)$, then multiply by $\aNrm$ to recover the optimal $\cNrm$.

4. Find the associated decision-time state by inverting the intraperiod budget: $\mNrm_t = \aNrm_t + \cNrm_t$.

5. Construct the consumption function as a linear interpolant over those $(\mNrm_t, \cNrm_t)$ pairs, adding a point at $(0,0)$ to incorporate the liquidity-constrained portion of the consumption function.

6. Construct the marginal value function $\vFunc'_t(\mNrm_t)$ as the composition of the marginal utility function and the consumption function.

Numerically solving the wealth-in-utility model is thus *barely* more computationally burdensome than solving the basic life-cycle model, despite the considerably more complex preferences.
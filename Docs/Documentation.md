# Documentation

## Preface

This repository is meant mostly as a learning project on low discrepancy sampling and importance sampling, as well as its computational implementation. To apply it to real world scenarios, the classic example of European options pricing under Black-Scholes hypothesis is taken, as it is a fundational benchmark for these methods.

The goal is to provide an incremental approach, starting from the analytical solution to the Black-Scholes model, as well as its Monte Carlo comptutational implementation, to then extend it to various Quasi Monte Carlo techniques, as well as variance reduction and importance sampling techniques. Further along, the hypothesis and assumptions of Black Scholes will be changed and made more strict, to get more complex, but more realistic, models.

Most of the Python implementations will use the functions given by the NumPy and SciPy modules, due to their stability and speed. Nonetheless, the reasoning behind the techniques here used are applicable to any language, as well as implementations from scratch.

## Introduction

**European options** are a type of financial derivative that give the holder the **right**, but not the obligation, to buy or sell an underlying asset at a predetermined **strike price** on a specific **expiration date**. A European **call option** allows the purchase of the asset at maturity, while a European **put option** allows its sale. Unlike American options, European options can only be exercised at expiration, which makes them easier to analyze mathematically.

The **Black–Scholes** model is one of the most important frameworks for pricing European options. Developed by Fischer Black, Myron Scholes, and Robert Merton in the early 1970s, the model provides a **closed-form** mathematical formula for determining the theoretical value of European call and put options. The model assumes that markets are **efficient** and that investors can continuously hedge risk by **dynamically adjusting positions** in the underlying asset. Because European options have a fixed exercise date, the Black–Scholes framework applies particularly well to them.

The Black–Scholes model relies on several **simplificative hypotheses**. First, it assumes that the price of the underlying asset follows a continuous stochastic process known as **geometric Brownian motion**, implying that returns are normally distributed and volatility remains constant over time. It also assumes frictionless markets, meaning there are no transaction costs, taxes, or restrictions on short selling. Additionally, the model considers a **constant risk-free interest rate** and assumes that trading can occur continuously. Another key assumption is that the underlying asset does not pay dividends during the option’s life, although later extensions of the model incorporate dividend payments.

## Black-Scholes model

The Black-Scholes model determines the fair price for an option (premium), in order to assume no expected net gain after its madurity. It works under the aforementioned assumptions. Its mathematical expression is

$$
C(S_0, K, T, r, \sigma) = S_0 \Phi(d_1) - K e^{-rT} \Phi(d_2)
$$

where

$$
d_1 = \frac{ \ln\left(\frac{S_0}{K}\right) + \left(r + \frac{1}{2}\sigma^2\right)T }{ \sigma \sqrt{T} }
$$

and
$$
d_2 = d_1 - \sigma \sqrt{T}
$$

or equivalently,

$$
d_2 =\frac{ \ln\left(\frac{S_0}{K}\right) + \left(r - \frac{1}{2}\sigma^2\right)T }{ \sigma \sqrt{T} }
$$

Its parameters are

- $S_0$: current stock price
- $K$: strike price
- $T$: time to maturity (in years)
- $r$: continuously compounded risk-free interest rate
- $\sigma$: volatility of the underlying asset
- $\Phi(\cdot)$: cumulative distribution function (CDF) of the standard normal distribution

This is the closed formula for the Black-Scholes model, and will be used as a benchmark for all the following methods. This way, these methods can be compared on a problem with known solution, and then exptrapolated to other assumptions or more exotic options.

This benchmark function is implemented inside the `Benchmark.py` file, under the name `european_call_cf(S0, K, T, r, sigma)`.

## Monte Carlo implementation

One of the assumptions for Black-Scholes is that stock prices follow Geometric Brownian Movement. Thus, given the same parameters as the previous model, one could simulate several possible paths for the stocks, and decide at maturity, given the stock price and strike price, wether or not it will be profitable to execute the option, as well as the payoff. Taking into consideration the depreciation of assets due to the risk free interest rate, one can aproximate the fair price for an option. The additional parameter needed to impelment this procedure is the number of iterations, this is, the number of stock paths simulated.

When normally distributed random numbers are used, it is called Monte Carlo simulation, and it is the simplest computational implementation of Black-Scholes. This function is implemented inside `MC_BlackScholes.py` as `european_call_mc(S0, K, T, r, sigma, n)`. This file also contains the Monte Carlo expected return, `expected_profit_mc( S0, K, T, r, sigma, option_price, n)`, which, using the same logic, takes option price as an input, simulates $n$ stock prices, and returns the expected profit over $n$ iterations.

For values close to the ones given by `european_cal_mc`, it will return values close to 0, as the option price obtained is the fair price. For lower option prices, expected values will generally be positive, and for higher option prices, they will generally be negative.

### Monte Carlo convergence

One of the aspects that will be improved on along the following implemenations will be the convergence rate. Given a theoretical exact value $\bar x$ and the sequence of Monte Carlo aproximations $\{ x_n\}_n$ using $n$ points, the following is true,

$$
\lim_n |\bar x-x_n|=0
$$

Thus, the Monte Carlo method will provide increasingly good aproximations. Nonetheless, the rate of convergence will be of the order of $\frac{1}{\sqrt{n}}$, so the method has an order of convergence $\mathcal{O}(n^{-\frac12})$.

# Documentation

## Preface

This repository is meant mostly as a learning project on low discrepancy sampling and importance sampling, as well as its computational implementation. To apply it to real world scenarios, the classic example of European options pricing under Black-Scholes hypothesis is taken, as it is a fundational benchmark for these methods.

The goal is to provide an incremental approach, starting from the analytical solution to the Black-Scholes model, as well as its Monte Carlo comptutational implementation, to then extend it to various Quasi Monte Carlo techniques, as well as variance reduction and importance sampling techniques. Further along, the hypothesis and assumptions of Black Scholes will be changed and made more strict, to get more complex, but more realistic, models.

Most of the Python implementations will use the functions given by the NumPy and SciPy modules, due to their stability and speed. Nonetheless, the reasoning behind the techniques here used are applicable to any language, as well as implementations from scratch. Unless otherwise stated, rounding error, as well as error atributed to the NumPy functions (number generation not being perfectly random or normal, inverse cdf having slight error,...) will be neglected, so exact values found through closed form solutions will be considered perfectly exact, and inconsistencies will not be atributed to machine precision. This is clearly an assumption, but generally, the magnitude of error will be considerably bigger than machine precision, making this assumption valid.

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

When normally distributed random numbers are used, it is called Monte Carlo simulation, and it is the simplest computational implementation of Black-Scholes. This function is implemented inside `MC_BlackScholes.py` as `european_call_mc(S0, K, T, r, sigma, n)`. The program returns the calculated value for the option price. This file also contains the Monte Carlo expected return, `expected_profit_mc( S0, K, T, r, sigma, option_price, n)`, which, using the same logic, takes option price as an input, simulates $n$ stock prices, and returns the expected profit over $n$ iterations.

By default, the programs run a single time, but and aditional argument `exp` can be added to run various experiments with the same parameters, and return a vector of experiments. Vectorizing the program twice (samples and experiments) is faster that using for loops for experiments, as numpy runs on C, so making less calls to the Python interpreter, while inputing bigger matrices (rather than vectors) is faster. However, for really big batches, RAM will become a limitation faster with this double vectorization, as the whole matrix will be bigger than running each vector separately.

For values close to the ones given by `european_cal_mc`, it will return values close to 0, as the option price obtained is the fair price. For lower option prices, expected values will generally be positive, and for higher option prices, they will generally be negative.

### Monte Carlo convergence

One of the aspects that will be improved on along the following implemenations will be the convergence rate. Given a theoretical exact value $\bar x$ and the sequence of Monte Carlo aproximations $\{ x_n\}_n$ using $n$ points, the following is true,

$$
\lim_n |\bar x-x_n|=0
$$

Thus, the Monte Carlo method will provide increasingly good aproximations. Nonetheless, the rate of convergence will be of the order of $\frac{1}{\sqrt{n}}$, so the method has an order of convergence $\mathcal{O}(n^{-\frac12})$. Let

$$
E_n\equiv |\bar{x}-x_n|=\frac{C}{\sqrt{n}}
$$

for some value of $C\in\mathbb{R}$. Then, $\log E_n=-\frac12\log n+\log C$. Therefore, the log-log plot of the error versus the sample size should be linear. For some given parameters (detailed in `MonteCarlo_Convergence.ipynb`), the Monte Carlo error rate is represented for certain values of $N$ (sample size), taking the average over 100 experiments. The 95% confidence interval bars are also shown.

![Monte Carlo Convergence rate](/Assets/MC_Convergence.png)

Additionally, the three defining metrics that will be used on these methods can be introduced. These are the Bias, variance and RMSE (root mean squared error).

**Bias** measures the **systematic error** introduced by approximating a real-world problem with a simplified model. It reflects how far the average prediction is from the true value.

$$
\text{Bias}(x) = \mathbb{E}[x] - \bar x
$$

**Variance** measures how much the model’s predictions **fluctuate** when trained on different datasets. It reflects model sensitivity to data noise.

$$
\text{Variance}(x) = \mathbb{E}\big[(x - \mathbb{E}[x])^2\big]
$$

**RMSE** measures the **average magnitude of prediction errors**, giving higher weight to large errors. It combines both bias and variance effects.

$$
\text{RMSE} = \sqrt{\mathbb{E}\big[(\hat{x} - y)^2\big]}
$$

Generally,

- High bias → model is too simple (underfitting)
- Low bias → model closely captures the true relationship
- High variance → model is too complex (overfitting)
- Low variance → model is more stable across datasets
- Lower RMSE → better predictive accuracy (has the same units as the predicted magnitude)

Due to the fact that $\text{RMSE}^2\approx\text{Variance} + \text{Bias}^2$, generally $\text{Bias}^2$ will be plotted over $\text{Bias}$.

For this implementation using Monte Carlo simulation, these are the results obtanied, as well as its fitting lines

![Monte Carlo performance metrics](/Assets/MC_metrics.png)

*(note how $\text{Bias}^2$ fits to $1/n$, as $E_n\approx1/\sqrt{n}$)*

## Antithethic variates

Once the baseline Monte Carlo implementation is done and tested, the object of this repository can be expanded on. The goal now is to test various techniques that can be used to obtain Quasi Monte Carlo (QMC) simulations that reduce the variance over plain Monte Carlo, leading to better results on smaller sample sizes. The first one that will be implemented is the use of antithetic variates. The idea behind it is to generate a sample size $Z$ of $\frac n2$ samples instead of $n$, but simulate both the $Z$ and $-Z$ paths. This reduces the computational cost of the sample generation, and can noticeably reduce bias and variance on well behaved problems. However, it can break independence of samples, and distort estimates on certain problems. It is implemented as `european_call_at(S0, K, T, r, sigma, n)`, also having `exp` as an additional argument. With the same values as before, the metrics for antithetic variates are found. However, instead of assuming $\frac{C}{\sqrt n}$ or $\frac Cn$ for convergence, the least squares aproximation for the log-log plot is found (using an auxiliary function).

![Antithetic variates performance metrics](/Assets/AT_metrics.png)

Furthermore, the computation time and variance of Monte Carlo and antithetic variates can be compared. As expected, antithetic variates reduces both the variance and computation time.

![Antithetic variates vs Monte Carlo](/Assets/MC_AT.png)

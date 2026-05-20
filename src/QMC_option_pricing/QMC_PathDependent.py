import numpy as np
from scipy.stats import norm

def path_dependent_mc(S0, K, T, r, rho, timesteps, n, exp=1):
    """
    Monte Carlo price of a European call option under GBM volatility.
    """
    
    dt = T / timesteps
    prices = np.zeros(exp)

    for i in range(exp):

        # Correlated random shocks
        Z = np.random.randn(n, timesteps)
        U = np.random.randn(n, timesteps)

        # Generate stochastic volatility
        sigma = rho * Z + np.sqrt(1 - rho**2) * U

        # Ensure volatility stays positive
        sigma = np.abs(sigma)

        # Stock price paths
        ST = np.zeros((n, timesteps + 1))
        ST[:, 0] = S0

        for t in range(timesteps):
            ST[:, t + 1] = ST[:, t] * np.exp(
                (r - 0.5 * sigma[:, t]**2) * dt
                + sigma[:, t] * np.sqrt(dt) * Z[:, t]
            )

        payoffs = np.maximum(ST[:, -1] - K, 0)
        prices[i] = np.exp(-r * T) * np.mean(payoffs)

    return prices

def path_dependent_at(S0, K, T, r, rho, timesteps, n, exp=1):
    """
    Antithetic variates price of a European call option under GBM volatility.
    """

    dt = T / timesteps
    prices = np.zeros(exp)
    
    # Half paths because we generate antithetic pairs
    m = n // 2

    for i in range(exp):
        Z = np.random.randn(m, timesteps)
        U = np.random.randn(m, timesteps)

        # Antithetic shocks
        Z_a = -Z
        U_a = -U

        sigma = np.abs(rho * Z + np.sqrt(1 - rho**2) * U)
        sigma_a = np.abs(rho * Z_a + np.sqrt(1 - rho**2) * U_a)

        # Price paths
        ST = np.full((m, timesteps + 1), S0)
        ST_a = np.full((m, timesteps + 1), S0)

        for t in range(timesteps):

            ST[:, t + 1] = ST[:, t] * np.exp(
                (r - 0.5 * sigma[:, t]**2) * dt
                + sigma[:, t] * np.sqrt(dt) * Z[:, t]
            )

            ST_a[:, t + 1] = ST_a[:, t] * np.exp(
                (r - 0.5 * sigma_a[:, t]**2) * dt
                + sigma_a[:, t] * np.sqrt(dt) * Z_a[:, t]
            )

        payoff = np.maximum(ST[:, -1] - K, 0)
        payoff_a = np.maximum(ST_a[:, -1] - K, 0)

        # Antithetic estimator
        prices[i] = np.exp(-r * T) * np.mean(0.5 * (payoff + payoff_a))

    return prices


def path_dependent_cv(S0, K, T, r, rho, timesteps, n, exp=1):
    """
    Monte Carlo pricing with a pathwise volatility Black-Scholes control variate.
    Returns CV prices, MC prices,betas
    """

    dt = T / timesteps

    mc_prices = np.zeros(exp)
    cv_prices = np.zeros(exp)
    betas = np.zeros(exp)

    for i in range(exp):
        Z = np.random.randn(n, timesteps)
        U = np.random.randn(n, timesteps)

        # stochastic volatility
        sigma = ( rho * Z + np.sqrt(1 - rho**2) * U)
        sigma = np.abs(sigma)

        ST = np.full(n, S0)

        for t in range(timesteps):

            ST = np.exp(
                (r - 0.5 * sigma[:, t]**2) * dt
                + sigma[:, t] * np.sqrt(dt) * Z[:, t]
            )

        # discounted payoff
        X = np.exp(-r * T) * np.maximum(ST - K, 0)

        # integrated variance
        integrated_var = np.sum(sigma**2 * dt, axis=1)

        # effective volatility per path
        sigma_eff = np.sqrt(integrated_var / T)


        d1 = ( np.log(S0 / K) + (r + 0.5 * sigma_eff**2) * T) / (sigma_eff * np.sqrt(T))
        d2 = d1 - sigma_eff * np.sqrt(T)

        Y = ( S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))

        EY = np.mean(Y)

        beta = np.cov(X, Y)[0, 1] / np.var(Y)
        cv_estimator = X - beta * (Y - EY)

        mc_prices[i] = np.mean(X)
        cv_prices[i] = np.mean(cv_estimator)
        betas[i] = beta

    return cv_prices, mc_prices, betas
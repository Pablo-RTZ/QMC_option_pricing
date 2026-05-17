import numpy as np
from scipy.stats import norm

def european_call_is(S0, K, T, r, sigma, a, n, exp=1):
    """
    Monte Carlo price of a European call option under mean shifted Black-Scholes.
    """

    # Generate standard normal random variables
    Z = np.random.rand(n, exp)
    Z = norm.ppf(Z) + a

    # Simulate terminal stock prices
    ST = S0 * np.exp(
        (r - 0.5 * sigma**2) * T
        + sigma * np.sqrt(T) * Z
    )

    # Compute payoffs
    weights = np.exp(-a * Z + 0.5 * a**2)
    payoffs = np.maximum(ST - K, 0) * weights
    
    # Discount expected payoff
    price = np.exp(-r * T) * np.mean(payoffs, axis=0)
    
    return price
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


def european_call_ce(S0, K, T, r, sigma, n, exp=1, tol=1e-6, damp=0.7, maxiter=20):
    """
    Monte Carlo price of a European call option under cross entroy optimal mean shifted Black-Scholes.
    """
    
    a = 0

    for _ in range(maxiter):
        # Generate standard normal random variables
        Z = np.random.rand(n, exp)
        Z = norm.ppf(Z) + a

        # Simulate terminal stock prices
        ST = S0 * np.exp(
            (r - 0.5 * sigma**2) * T
                + sigma * np.sqrt(T) * Z
        )

        # Compute payoffs
        payoffs = np.maximum(ST - K, 0)

        if payoffs.sum() == 0:
            a += 1
            continue

        a_new = np.sum(payoffs*Z)/np.sum(payoffs)
        a_new = damp*a_new + (1-damp)*a

        if abs(a_new - a) < tol:
            a = a_new
            break

        a = a_new
    
    # Run final simulation with final mean shift
    Z = np.random.rand(n, exp)
    Z = norm.ppf(Z) + a

    # Simulate terminal stock prices
    ST = S0 * np.exp(
        (r - 0.5 * sigma**2) * T
            + sigma * np.sqrt(T) * Z
    )

    payoff = np.maximum(ST - K, 0)
    weights = np.exp(-a * Z + 0.5 * a**2)
    price = np.exp(-r * T) * np.mean(payoffs * weights, axis=0)
    
    return price, a
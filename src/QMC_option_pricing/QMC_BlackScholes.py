import numpy as np

def european_call_at(S0, K, T, r, sigma, n, exp=1):
    """
    Monte Carlo price of a European call option under Black-Scholes, using antithetic variates.
    """

    # Generate half of all samples, and use its antithetic points
    U = np.random.randn(round(n/2), exp)
    Z = np.concatenate([U,-U],axis=0)

    # Simulate terminal stock prices
    ST = S0 * np.exp(
        (r - 0.5 * sigma**2) * T
        + sigma * np.sqrt(T) * Z
    )

    # Compute payoffs
    payoffs = np.maximum(ST - K, 0)
    
    # Discount expected payoff
    price = np.exp(-r * T) * np.mean(payoffs, axis=0)
    
    return price
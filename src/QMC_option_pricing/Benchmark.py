import numpy as np
from scipy.stats import norm

def european_call_cf(S0, K, T, r, sigma):
    """
    Black-Scholes closed form analytical price of a European call option.
    """

    if T <= 0:
        return max(S0 - K, 0)

    # Step 1: Compute d1 and d2
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Step 2: Compute call price
    call_price = (
        S0 * norm.cdf(d1)
        - K * np.exp(-r * T) * norm.cdf(d2)
    )

    return call_price
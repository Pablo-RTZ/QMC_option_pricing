import numpy as np

def european_call_mc(S0, K, T, r, sigma, n):
    """
    Monte Carlo price of a European call option under Black-Scholes.
    """

    # Generate standard normal random variables
    Z = np.random.randn(n)

    # Simulate terminal stock prices
    ST = S0 * np.exp(
        (r - 0.5 * sigma**2) * T
        + sigma * np.sqrt(T) * Z
    )

    # Compute payoffs
    payoffs = np.maximum(ST - K, 0)

    # Discount expected payoff
    price = np.exp(-r * T) * np.mean(payoffs)

    return price


def expected_profit_mc( S0, K, T, r, sigma, option_price, n):
    """
    Monte Carlo estimated profit of a European call option under Black-Scholes (risk neutral).
    """
    Z = np.random.randn(n)

    ST = S0 * np.exp(
        (r - 0.5 * sigma**2) * T
        + sigma * np.sqrt(T) * Z
    )

    payoffs = np.maximum(ST - K, 0)

    # Profit at maturity
    profits_T = payoffs - option_price * np.exp(r * T)

    expected_profit_T = np.mean(profits_T)

    return expected_profit_T
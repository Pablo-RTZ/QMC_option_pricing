import numpy as np
from scipy.stats import norm
from scipy.stats.qmc import Sobol,Halton

def Kronecker(m,n):
    """
    Generates a mxn array of points using Kronecker sequences (golden ratio conjugate)
    """
    n = int(n)
    m = int(m)

    alpha = (np.sqrt(5)-1)/2
    V = alpha * np.arange(m*n) % 1.0
    return V.reshape(n,m).T

def european_call_at(S0, K, T, r, sigma, n, exp=1):
    """
    Monte Carlo price of a European call option under Black-Scholes, using antithetic variates.
    """

    # Generate half of all samples, and use its antithetic points
    U = np.random.rand(round(n/2), exp)
    U = norm.ppf(U)
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

def european_call_ss(S0, K, T, r, sigma, n, bins, exp=1):
    """
    Monte Carlo price of a European call option under Black-Scholes, using stratified sampling.
    """

    # Split the [0,1] domain into bins, generate random points, and inverse CDF them
    x = np.linspace(0,1,bins+1)
    Z = []
    for i in range(bins):
        U = x[i] + 1/bins*np.random.rand(n//bins, exp)
        Z.append(U)
    
    Z = np.concatenate(Z, axis=0)
    Z = norm.ppf(Z)

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

def european_call_kr(S0, K, T, r, sigma, n, exp=1):
    """
    Monte Carlo price of a European call option under Black-Scholes, using kronecker sequences.
    """

    Z = Kronecker(n,exp)
    Z = norm.ppf(Z)

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

def european_call_halton(S0, K, T, r, sigma, n, exp=1):
    """
    Monte Carlo price of a European call option under Black-Scholes, using halton sequences.
    """

    Z = Halton(d=exp).random(n=n)
    Z = norm.ppf(Z)

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

def european_call_sobol(S0, K, T, r, sigma, n, exp=1):
    """
    Monte Carlo price of a European call option under Black-Scholes, using sobol sequences.
    """

    Z = Sobol(d=exp).random(n=n)
    Z = norm.ppf(Z)

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
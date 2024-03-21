import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    return vega

def calculate_implied_volatility(option_price, S, K, T, r, max_iterations=100, precision=1e-6):
    """
    Calculate implied volatility using the Newton-Raphson method.
    """
    sigma = 0.5  # Initial guess for implied volatility
    
    for i in range(max_iterations):
        # Calculate the option price using the current sigma estimate
        bs_price = black_scholes_call(S, K, T, r, sigma)
        
        # Calculate the vega for the current sigma estimate
        bs_vega = vega(S, K, T, r, sigma)
        
        # Calculate the difference between the market price and the estimated price
        diff = option_price - bs_price
        
        # Check if the difference is within the desired precision
        if abs(diff) < precision:
            return sigma
        
        # Update the sigma estimate using the Newton-Raphson formula
        sigma = sigma + diff / bs_vega
    
    # Return the final sigma estimate if the maximum iterations are reached
    return sigma
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm

def low_risk_short_wait(underlying_symbol, expiry_date, risk_free_rate, iv_threshold=0.4, otm_threshold=0.05):
    """
    Low risk, short wait time, good reward strategy.
    """
    # Fetch option chain data for the given underlying symbol and expiry date using yfinance
    stock = yf.Ticker(underlying_symbol)
    expiry_dates = stock.options
    
    if expiry_date not in expiry_dates:
        raise ValueError(f"Expiry date {expiry_date} not available for {underlying_symbol}")
    
    try:
        option_chain = stock.option_chain(expiry_date)
    except Exception as e:
        print(f"Error decoding JSON response: {e}")

    calls = option_chain.calls
    puts = option_chain.puts
    
    # Get the current underlying price
    if 'regularMarketPrice' in stock.info:
        underlying_price = stock.info['regularMarketPrice']
    elif 'currentPrice' in stock.info:
        underlying_price = stock.info['currentPrice']
    else:
        raise KeyError("Unable to retrieve the current market price.")
    
    # Calculate time to expiry in years
    expiry_date_obj = pd.to_datetime(expiry_date)
    time_to_expiry = (expiry_date_obj - pd.Timestamp.today()).days / 365
    
    # Filter options with short expiry (e.g., 30-45 days) and low implied volatility
    short_expiry_calls = calls[(calls['impliedVolatility'] < iv_threshold) & (time_to_expiry >= 30/365) & (time_to_expiry <= 45/365)]
    short_expiry_puts = puts[(puts['impliedVolatility'] < iv_threshold) & (time_to_expiry >= 30/365) & (time_to_expiry <= 45/365)]
    
    # Select options with strike prices close to the current underlying price
    otm_calls = short_expiry_calls[(short_expiry_calls['strike'] > underlying_price) & ((short_expiry_calls['strike'] - underlying_price) / underlying_price <= otm_threshold)]
    otm_puts = short_expiry_puts[(short_expiry_puts['strike'] < underlying_price) & ((underlying_price - short_expiry_puts['strike']) / underlying_price <= otm_threshold)]
    
    # Calculate the expected return for each option
    otm_calls['expected_return'] = otm_calls.apply(lambda row: (row['bid'] + row['ask']) / 2 * norm.cdf(d1(underlying_price, row['strike'], time_to_expiry, risk_free_rate, row['impliedVolatility'])), axis=1)
    otm_puts['expected_return'] = otm_puts.apply(lambda row: (row['bid'] + row['ask']) / 2 * norm.cdf(-d1(underlying_price, row['strike'], time_to_expiry, risk_free_rate, row['impliedVolatility'])), axis=1)
    
    # print("Short expiry calls:")
    # print(short_expiry_calls)
    # print("Short expiry puts:")
    # print(short_expiry_puts)
    # print("OTM calls:")
    # print(otm_calls)
    # print("OTM puts:")
    # print(otm_puts)

    # Combine the calls and puts dataframes
    selected_options = pd.concat([otm_calls, otm_puts])
    
    # Calculate the total expected return
    total_expected_return = selected_options['expected_return'].sum()
    
    return selected_options, total_expected_return

def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

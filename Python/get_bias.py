import numpy as np
import pandas as pd
import yfinance as yf
from hurst import compute_Hc
from statsmodels.tsa.stattools import adfuller
from datetime import datetime, timedelta

def calculate_hurst_exponent(data):
    H, _, _ = compute_Hc(data, kind='price', simplified=True)
    return H

def perform_adf_test(data):
    result = adfuller(data)
    return result[1]  # p-value

def calculate_returns(data):
    return np.log(data / data.shift(1)).dropna()

def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date, interval='1h', progress=False)
    return data['Close']

def analyze_asset(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Fetch 30 days of data
    
    prices = fetch_data(ticker, start_date, end_date)
    
    # Use the last 5 days (120 hours) for analysis
    analysis_window = prices.iloc[-120:]
    returns = calculate_returns(analysis_window)
    
    H = calculate_hurst_exponent(analysis_window)
    adf_p = perform_adf_test(analysis_window)
    recent_return = returns.mean()
    recent_volatility = returns.std() * np.sqrt(252 * 24)  # Annualized volatility
    
    return H, adf_p, recent_return, recent_volatility

def interpret_results(H, adf_p, recent_return, recent_volatility):
    if H > 0.6:
        hurst_interp = "strongly trending"
    elif 0.5 < H <= 0.6:
        hurst_interp = "weakly trending"
    elif 0.4 <= H <= 0.5:
        hurst_interp = "ranging"
    else:
        hurst_interp = "mean-reverting"
    
    adf_interp = "stationary" if adf_p < 0.05 else "non-stationary"
    
    if recent_return > 0:
        direction = "upward"
    elif recent_return < 0:
        direction = "downward"
    else:
        direction = "neutral"
    
    volatility_level = "high" if recent_volatility > 0.3 else "low"
    
    return hurst_interp, adf_interp, direction, volatility_level

tickers = {
    'Gold': 'GC=F',
    'Corn': 'ZC=F',
    'Japanese Yen': '6J=F',
    'Oil': 'CL=F',
    'S&P500': 'ES=F'
}

for asset_name, ticker in tickers.items():
    try:
        H, adf_p, recent_return, recent_volatility = analyze_asset(ticker)
        hurst_interp, adf_interp, direction, volatility_level = interpret_results(H, adf_p, recent_return, recent_volatility)
        
        print(f"{asset_name} ({ticker}) 5-Day Analysis:")
        print(f"Hurst exponent: {H:.4f} ({hurst_interp})")
        print(f"ADF test: {adf_p:.1%} ({adf_interp})")
        print(f"Short-term direction: {direction}")
        print(f"Volatility level: {volatility_level}")
        print(f"Recent return: {recent_return:.2%}")
        print(f"Recent volatility: {recent_volatility:.2%} (annualized)")
        print()
    except Exception as e:
        print(f"Error analyzing {asset_name} ({ticker}): {str(e)}")
        print()

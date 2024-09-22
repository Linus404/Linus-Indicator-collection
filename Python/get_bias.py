import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from hurst import compute_Hc

# Function to calculate the average candle volatility (in %)
def calculate_average_volatility(data):
    candle_volatility = ((data['High'] - data['Low']) / data['Close']) * 100
    average_volatility = candle_volatility.mean()
    return average_volatility

# Function to calculate the Hurst exponent
def calculate_hurst_exponent(data):
    H, _, _ = compute_Hc(data, kind='price', simplified=True)
    return H

# Function to fetch 30-minute data for 5-day analysis
def fetch_data_30min(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date, interval='30m', progress=False)

# Function to fetch 1-hour data for 30-day analysis
def fetch_data_1h(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date, interval='1h', progress=False)

# Analyze 5-day volatility and Hurst exponent using 30-minute bars
def analyze_5d(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)
    prices = fetch_data_30min(ticker, start_date, end_date)
    volatility = calculate_average_volatility(prices)
    hurst = calculate_hurst_exponent(prices['Close'].values)
    return volatility, hurst

# Analyze 30-day volatility and Hurst exponent using 1-hour bars
def analyze_30d(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    prices = fetch_data_1h(ticker, start_date, end_date)
    volatility = calculate_average_volatility(prices)
    hurst = calculate_hurst_exponent(prices['Close'].values)
    return volatility, hurst

# Function to run analysis for all assets and return results
def analyze_assets():
    tickers = {
        'Gold': 'GC=F',
        'Jap Yen': '6J=F',
        'Oil': 'CL=F',
        'S&P500': 'ES=F',
        'Gas': 'NG=F'
    }
    
    results = []
    
    for asset_name, ticker in tickers.items():
        try:
            vol_5d, hurst_5d = analyze_5d(ticker)
            vol_30d, hurst_30d = analyze_30d(ticker)
            
            results.append({
                'Asset': asset_name,
                'Volatility (5D)': f"{vol_5d:.2f}%",
                'Volatility (30D)': f"{vol_30d:.2f}%",
                'Hurst (5D)': f"{hurst_5d:.4f}",
                'Hurst (30D)': f"{hurst_30d:.4f}"
            })
        
        except Exception as e:
            results.append({
                'Asset': asset_name,
                'Volatility (5D)': 'Error',
                'Volatility (30D)': 'Error',
                'Hurst (5D)': 'Error',
                'Hurst (30D)': 'Error'
            })
    
    return results

# Function to display results in a tkinter window
def display_results():
    results = analyze_assets()
    
    # Create main window
    window = tk.Tk()
    window.title("Market Analysis Results")
    
    # Create a table with columns for the analysis results
    columns = ("Asset", "Volatility (5D)", "Volatility (30D)", "Hurst (5D)", "Hurst (30D)")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    
    # Define headings
    for col in columns:
        tree.heading(col, text=col)
    
    # Insert data into the table
    for result in results:
        tree.insert("", "end", values=(result["Asset"], result["Volatility (5D)"], result["Volatility (30D)"], 
                                       result["Hurst (5D)"], result["Hurst (30D)"]))
    
    # Pack the table into the window and expand
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Set column widths
    for col in columns:
        tree.column(col, width=150)
    
    # Run the tkinter main loop
    window.geometry("900x250")
    window.mainloop()

# Run the display function
display_results()

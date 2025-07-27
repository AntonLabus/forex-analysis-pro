#!/usr/bin/env python3
"""
Test script to get real current EUR/USD price from Yahoo Finance
"""

import yfinance as yf
from datetime import datetime

def test_yahoo_price():
    try:
        print("Testing Yahoo Finance API...")
        
        # Get EUR/USD data
        ticker = yf.Ticker('EURUSD=X')
        data = ticker.history(period='1d')
        
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            print(f"EUR/USD current price: {current_price:.4f}")
            print(f"Last update: {datetime.now()}")
            
            # Also test info
            info = ticker.info
            if 'regularMarketPrice' in info:
                print(f"Regular market price: {info['regularMarketPrice']:.4f}")
                
        else:
            print("No data received from Yahoo Finance")
            
    except Exception as e:
        print(f"Error testing Yahoo Finance: {e}")

if __name__ == "__main__":
    test_yahoo_price()

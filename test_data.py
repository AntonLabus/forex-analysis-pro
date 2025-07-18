"""
Quick test to verify data fetching is working
"""

import yfinance as yf
import requests
from datetime import datetime

def test_yfinance():
    """Test Yahoo Finance data fetching"""
    print("Testing Yahoo Finance...")
    
    try:
        # Test EUR/USD
        ticker = yf.Ticker("EURUSD=X")
        hist = ticker.history(period="1d", interval="1h")
        
        if not hist.empty:
            latest_price = hist['Close'].iloc[-1]
            print(f"✓ EUR/USD current price: {latest_price:.5f}")
            return True
        else:
            print("✗ No data received from Yahoo Finance")
            return False
            
    except Exception as e:
        print(f"✗ Yahoo Finance error: {e}")
        return False

def test_alternative_api():
    """Test alternative forex API"""
    print("\nTesting alternative API...")
    
    try:
        # Free forex API
        url = "https://api.exchangerate-api.com/v4/latest/EUR"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            usd_rate = data['rates']['USD']
            print(f"✓ EUR/USD rate: {usd_rate:.5f}")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Alternative API error: {e}")
        return False

def main():
    print("="*50)
    print("Forex Data Fetching Test")
    print("="*50)
    
    yf_works = test_yfinance()
    alt_works = test_alternative_api()
    
    print("\n" + "="*50)
    print("Summary:")
    print(f"Yahoo Finance: {'✓ Working' if yf_works else '✗ Failed'}")
    print(f"Alternative API: {'✓ Working' if alt_works else '✗ Failed'}")
    
    if yf_works or alt_works:
        print("\n🎉 At least one data source is working!")
    else:
        print("\n❌ All data sources failed. Check internet connection.")
    
    print("="*50)

if __name__ == "__main__":
    main()

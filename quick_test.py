"""
Quick forex data test
"""
import requests
import yfinance as yf

print("=== Forex Data Source Test ===")

# Test ExchangeRate-API
print("\n1. Testing ExchangeRate-API...")
try:
    r = requests.get('https://api.exchangerate-api.com/v4/latest/EUR', timeout=10)
    data = r.json()
    eurusd = data['rates']['USD']
    print(f"   ✅ EUR/USD: {eurusd:.5f}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test Yahoo Finance
print("\n2. Testing Yahoo Finance...")
try:
    ticker = yf.Ticker("EURUSD=X")
    hist = ticker.history(period="1d")
    if not hist.empty:
        price = hist['Close'].iloc[-1]
        print(f"   ✅ EUR/USD: {price:.5f}")
    else:
        print("   ❌ No data returned")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n=== Test Complete ===")

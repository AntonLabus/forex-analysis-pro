"""
Real-time forex data source tester
Tests all available data sources to show which ones are working
"""

import requests
import yfinance as yf
from datetime import datetime
import json

def test_yahoo_finance():
    """Test Yahoo Finance"""
    print("🔍 Testing Yahoo Finance...")
    try:
        ticker = yf.Ticker("EURUSD=X")
        hist = ticker.history(period="1d", interval="5m")
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            print(f"   ✅ EUR/USD: {price:.5f}")
            return True, price
        else:
            print("   ❌ No data returned")
            return False, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def test_exchangerate_api():
    """Test ExchangeRate-API (free)"""
    print("🔍 Testing ExchangeRate-API...")
    try:
        url = "https://api.exchangerate-api.com/v4/latest/EUR"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'rates' in data and 'USD' in data['rates']:
                price = data['rates']['USD']
                print(f"   ✅ EUR/USD: {price:.5f}")
                return True, price
        print(f"   ❌ API returned status: {response.status_code}")
        return False, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def test_fixer_io():
    """Test Fixer.io (requires API key)"""
    print("🔍 Testing Fixer.io...")
    try:
        # Using the free endpoint (limited)
        url = "https://api.fixer.io/latest?base=EUR&symbols=USD"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'rates' in data and 'USD' in data['rates']:
                price = data['rates']['USD']
                print(f"   ✅ EUR/USD: {price:.5f}")
                return True, price
        print(f"   ❌ API returned status: {response.status_code}")
        return False, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def test_financial_modeling_prep():
    """Test Financial Modeling Prep (demo)"""
    print("🔍 Testing Financial Modeling Prep...")
    try:
        url = "https://financialmodelingprep.com/api/v3/fx/EURUSD?apikey=demo"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                # Try different price fields
                price = None
                for field in ['bid', 'ask', 'price', 'rate']:
                    if field in data[0]:
                        price = data[0][field]
                        break
                
                if price:
                    print(f"   ✅ EUR/USD: {price:.5f}")
                    return True, price
        print(f"   ❌ API returned status: {response.status_code}")
        return False, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def test_currency_beacon():
    """Test CurrencyBeacon (free tier)"""
    print("🔍 Testing CurrencyBeacon...")
    try:
        url = "https://api.currencybeacon.com/v1/latest?base=EUR&symbols=USD"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'rates' in data and 'USD' in data['rates']:
                price = data['rates']['USD']
                print(f"   ✅ EUR/USD: {price:.5f}")
                return True, price
        print(f"   ❌ API returned status: {response.status_code}")
        return False, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def main():
    print("=" * 60)
    print("🚀 FOREX DATA SOURCES TEST")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    working_sources = []
    prices = {}
    
    # Test all sources
    sources = [
        ("Yahoo Finance", test_yahoo_finance),
        ("ExchangeRate-API", test_exchangerate_api),
        ("Fixer.io", test_fixer_io),
        ("Financial Modeling Prep", test_financial_modeling_prep),
        ("CurrencyBeacon", test_currency_beacon),
    ]
    
    for name, test_func in sources:
        success, price = test_func()
        if success:
            working_sources.append(name)
            prices[name] = price
        print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if working_sources:
        print(f"✅ Working sources: {len(working_sources)}/{len(sources)}")
        print()
        
        print("🏆 EUR/USD prices from working sources:")
        for source in working_sources:
            print(f"   {source}: {prices[source]:.5f}")
        
        if len(working_sources) > 1:
            avg_price = sum(prices.values()) / len(prices)
            print(f"\n📈 Average price: {avg_price:.5f}")
            
            # Check for significant differences
            min_price = min(prices.values())
            max_price = max(prices.values())
            spread = max_price - min_price
            
            if spread > 0.001:  # More than 0.1 cent difference
                print(f"⚠️  Price spread: {spread:.5f} (sources may have different update times)")
            else:
                print("✅ Prices are consistent across sources")
        
        print(f"\n🎉 RECOMMENDATION: Use {working_sources[0]} as primary data source")
        
    else:
        print("❌ NO WORKING SOURCES FOUND")
        print("\n🔧 Troubleshooting:")
        print("   1. Check internet connection")
        print("   2. Verify firewall settings")
        print("   3. Try again in a few minutes (rate limiting)")
        print("   4. Consider getting API keys for premium access")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Simple API test script
"""

import requests
import json

def test_crypto_apis():
    """Test crypto APIs directly"""
    print("=== Testing Crypto APIs ===")
    
    # Test CoinGecko
    print("\n🦎 Testing CoinGecko API:")
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ CoinGecko Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ CoinGecko Failed: {response.text}")
    except Exception as e:
        print(f"❌ CoinGecko Exception: {e}")
    
    # Test Binance
    print("\n🟡 Testing Binance API:")
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Binance Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Binance Failed: {response.text}")
    except Exception as e:
        print(f"❌ Binance Exception: {e}")

def test_forex_apis():
    """Test forex APIs directly"""
    print("\n=== Testing Forex APIs ===")
    
    # Test ExchangeRate API
    print("\n💱 Testing ExchangeRate API:")
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})
            eur_rate = rates.get('EUR', 'Not found')
            print(f"✅ EUR/USD Rate: {eur_rate}")
        else:
            print(f"❌ ExchangeRate API Failed: {response.text}")
    except Exception as e:
        print(f"❌ ExchangeRate API Exception: {e}")

if __name__ == "__main__":
    test_crypto_apis()
    test_forex_apis()

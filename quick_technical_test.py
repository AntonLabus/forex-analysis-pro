#!/usr/bin/env python3
import requests

def test_btc():
    try:
        response = requests.get("http://localhost:5000/api/analysis/technical/BTCUSD?timeframe=1h", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ BTCUSD technical analysis working!")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_btc()

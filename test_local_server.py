#!/usr/bin/env python3
"""
Test the local server endpoints
"""

import requests
import json

def test_local_server():
    """Test the local server crypto endpoint"""
    
    base_url = "http://localhost:5000"
    
    print("=== Testing Local Server ===")
    
    # Test basic server health
    try:
        response = requests.get(f"{base_url}/api/test", timeout=5)
        print(f"✅ Server health: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Server health check failed: {e}")
        return False
    
    # Test forex pairs endpoint
    try:
        response = requests.get(f"{base_url}/api/forex/pairs?market_type=forex", timeout=10)
        print(f"\n📈 Forex endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Forex pairs count: {len(data.get('data', []))}")
        else:
            print(f"Forex error: {response.text}")
    except Exception as e:
        print(f"❌ Forex test failed: {e}")
    
    # Test crypto pairs endpoint
    try:
        response = requests.get(f"{base_url}/api/forex/pairs?market_type=crypto", timeout=15)
        print(f"\n🪙 Crypto endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Crypto pairs count: {len(data.get('data', []))}")
            print(f"Market type returned: {data.get('market_type')}")
            if data.get('data'):
                print(f"First crypto pair: {data['data'][0].get('symbol')}")
        else:
            print(f"❌ Crypto error: {response.text}")
    except Exception as e:
        print(f"❌ Crypto test failed: {e}")
    
    # Test technical analysis for crypto
    try:
        response = requests.get(f"{base_url}/api/analysis/technical/BTCUSD?timeframe=1h", timeout=10)
        print(f"\n🔍 Technical analysis BTCUSD: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis success: {data.get('success')}")
            print(f"Data source: {data.get('analysis', {}).get('data_source', 'unknown')}")
        else:
            print(f"❌ Technical analysis error: {response.text}")
    except Exception as e:
        print(f"❌ Technical analysis test failed: {e}")
    
    # Test technical analysis for forex
    try:
        response = requests.get(f"{base_url}/api/analysis/technical/EURUSD?timeframe=1h", timeout=10)
        print(f"\n🔍 Technical analysis EURUSD: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis success: {data.get('success')}")
            print(f"Data source: {data.get('analysis', {}).get('data_source', 'unknown')}")
        else:
            print(f"❌ Technical analysis error: {response.text}")
    except Exception as e:
        print(f"❌ Technical analysis test failed: {e}")

if __name__ == "__main__":
    test_local_server()

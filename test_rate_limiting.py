#!/usr/bin/env python3
"""
Test script for the enhanced rate limiting system
Tests all new endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, description):
    """Test an API endpoint and display results"""
    print(f"\n🔍 Testing {description}")
    print(f"Endpoint: {endpoint}")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Success!")
                print(json.dumps(data, indent=2))
            except json.JSONDecodeError as e:
                print(f"❌ JSON Error: {e}")
                print(f"Raw Response: {response.text}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")

def main():
    print("=" * 60)
    print("  FOREX ANALYSIS PRO - RATE LIMITING SYSTEM TEST")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test basic endpoints
    test_endpoint("/api/health", "Basic Health Check")
    
    # Test new rate limiting endpoints
    test_endpoint("/api/system/rate-limits", "Rate Limits Status")
    test_endpoint("/api/system/health", "System Health Monitoring")
    
    # Test some data endpoints to generate API usage
    test_endpoint("/api/forex/pairs", "Forex Pairs (to generate API usage)")
    test_endpoint("/api/signals", "Trading Signals")
    
    # Test rate limits again to see if usage has changed
    print("\n" + "=" * 60)
    print("  CHECKING RATE LIMITS AFTER API USAGE")
    print("=" * 60)
    test_endpoint("/api/system/rate-limits", "Rate Limits After Usage")
    test_endpoint("/api/system/health", "System Health After Usage")
    
    print("\n" + "=" * 60)
    print("  TEST COMPLETE")
    print("=" * 60)
    print("✅ If you see JSON responses above, the rate limiting system is working!")
    print("🎯 Check the monitor button in the web interface for real-time data")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Simple test script to verify the API is working with crypto pairs
"""
import requests
import json
import sys

def test_api():
    try:
        print("Testing local server at http://localhost:5000...")
        
        # Test emergency mode status
        print("\n1. Testing emergency mode status...")
        r = requests.get("http://localhost:5000/api/system/emergency-mode", timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print(f"Emergency mode: {r.json()}")
        
        # Test crypto pairs
        print("\n2. Testing crypto pairs...")
        r = requests.get("http://localhost:5000/api/forex/pairs?market_type=crypto", timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Received {len(data.get('pairs', []))} crypto pairs")
            print(f"First 3 pairs: {data.get('pairs', [])[:3]}")
        else:
            print(f"Error: {r.text}")
            
    except requests.exceptions.Timeout:
        print("Request timed out - server may be overloaded")
    except requests.exceptions.ConnectionError:
        print("Connection error - server may not be running")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()

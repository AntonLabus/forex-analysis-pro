#!/usr/bin/env python3
"""
Test script to verify the emergency fixes are working
"""
import requests
import time
import json

def test_emergency_fixes():
    try:
        print("Testing emergency fixes for production worker timeout issues...")
        
        # Test crypto pairs with timing
        print("\n1. Testing crypto pairs endpoint with timing...")
        start_time = time.time()
        
        r = requests.get("http://localhost:5000/api/forex/pairs?market_type=crypto", timeout=15)
        end_time = time.time()
        
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            print(f"Success: {data.get('success')}")
            print(f"Pairs returned: {len(data.get('data', []))}")
            print(f"Market type: {data.get('market_type')}")
            print(f"Source: {data.get('source', 'Unknown')}")
            
            if 'emergency_mode' in data:
                print(f"Emergency mode: {data['emergency_mode']}")
                
            if 'warning' in data:
                print(f"Warning: {data['warning']}")
                
            # Show first pair data
            if data.get('data'):
                first_pair = data['data'][0]
                print(f"First pair: {first_pair['symbol']} = ${first_pair['current_price']}")
                print(f"Data quality: {first_pair.get('data_quality', 'Unknown')}")
        else:
            print(f"Error: {r.text}")
            
        # Test emergency mode status
        print("\n2. Testing emergency mode status...")
        r = requests.get("http://localhost:5000/api/system/emergency-mode", timeout=5)
        if r.status_code == 200:
            status = r.json()
            print(f"Emergency mode active: {status.get('active', 'Unknown')}")
            print(f"Emergency until: {status.get('emergency_until', 'N/A')}")
        else:
            print(f"Emergency status check failed: {r.status_code}")
            
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out - may still have performance issues")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_emergency_fixes()

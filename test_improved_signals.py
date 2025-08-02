#!/usr/bin/env python3
"""
Test script to check the improved signal generation
"""
import requests
import time

def test_improved_signals():
    try:
        print("Testing improved signal generation (less HOLD bias)...")
        
        # Test multiple pairs to see signal variety
        pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']
        
        for pair in pairs:
            print(f"\n--- Testing {pair} ---")
            
            # Test current pairs endpoint
            r = requests.get(f"http://localhost:5000/api/forex/pairs?market_type=forex", timeout=10)
            if r.status_code == 200:
                data = r.json()
                
                # Find the pair in the response
                for pair_data in data.get('data', []):
                    if pair_data['symbol'] == pair:
                        print(f"Signal: {pair_data.get('technical_signal', 'N/A')}")
                        print(f"Confidence: {pair_data.get('confidence', 'N/A')}%")
                        print(f"Technical: {pair_data.get('technical_recommendation', 'N/A')}")
                        print(f"Fundamental: {pair_data.get('fundamental_recommendation', 'N/A')}")
                        break
            else:
                print(f"Error fetching data for {pair}: {r.status_code}")
            
            time.sleep(0.5)  # Small delay between requests
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_improved_signals()

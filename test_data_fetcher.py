#!/usr/bin/env python3
"""
Test the backend data fetcher directly
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.data_fetcher import DataFetcher

def test_data_fetcher():
    try:
        print("Testing DataFetcher...")
        fetcher = DataFetcher()
        
        # Test EUR/USD specifically
        price = fetcher.get_current_price('EURUSD')
        print(f"DataFetcher returned EUR/USD price: {price}")
        
        if price:
            print(f"Price type: {type(price)}")
            print(f"Formatted: {price:.4f}")
        else:
            print("DataFetcher returned None/empty")
            
    except Exception as e:
        print(f"Error testing DataFetcher: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_fetcher()

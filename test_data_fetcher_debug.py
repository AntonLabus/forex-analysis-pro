#!/usr/bin/env python3
"""
Test script to debug data fetcher issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.data_fetcher import DataFetcher
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_data_fetcher():
    """Test the data fetcher with both forex and crypto pairs"""
    
    print("=== Testing Data Fetcher ===")
    
    fetcher = DataFetcher()
    
    # Test forex pairs
    forex_pairs = ['EURUSD', 'GBPUSD']
    print(f"\n📈 Testing Forex Pairs: {forex_pairs}")
    
    for pair in forex_pairs:
        print(f"\n--- Testing {pair} ---")
        try:
            price = fetcher.get_current_price(pair)
            if price:
                print(f"✅ {pair}: ${price:.5f}")
            else:
                print(f"❌ {pair}: Failed to get price")
        except Exception as e:
            print(f"❌ {pair}: Exception - {e}")
    
    # Test crypto pairs
    crypto_pairs = ['BTCUSD', 'ETHUSD']
    print(f"\n🪙 Testing Crypto Pairs: {crypto_pairs}")
    
    for pair in crypto_pairs:
        print(f"\n--- Testing {pair} ---")
        try:
            price = fetcher.get_current_price(pair)
            if price:
                print(f"✅ {pair}: ${price:.2f}")
            else:
                print(f"❌ {pair}: Failed to get price")
        except Exception as e:
            print(f"❌ {pair}: Exception - {e}")
    
    # Test crypto detection
    print(f"\n🔍 Testing Crypto Detection:")
    test_pairs = ['BTCUSD', 'ETHUSD', 'EURUSD', 'GBPUSD']
    for pair in test_pairs:
        is_crypto = fetcher._is_crypto_pair(pair)
        print(f"{pair}: {'🪙 Crypto' if is_crypto else '📈 Forex'}")

if __name__ == "__main__":
    test_data_fetcher()

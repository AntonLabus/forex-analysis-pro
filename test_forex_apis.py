#!/usr/bin/env python3
"""
Quick test of real-time forex APIs to fix the price issue
"""

import requests
import json

def test_exchangerate_api():
    """Test the free exchangerate API"""
    try:
        print("Testing exchangerate-api.com...")
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10)
        data = response.json()
        
        if 'rates' in data and 'EUR' in data['rates']:
            eur_rate = data['rates']['EUR']
            eurusd_rate = 1 / eur_rate  # Convert USD->EUR rate to EUR->USD
            print(f"EUR/USD from exchangerate-api: {eurusd_rate:.4f}")
            return eurusd_rate
        else:
            print("No EUR rate in exchangerate-api response")
            
    except Exception as e:
        print(f"Error with exchangerate-api: {e}")
        
    return None

def test_fixer_api():
    """Test fixer.io API (free tier)"""
    try:
        print("Testing fixer.io...")
        # Note: fixer.io requires API key for HTTPS, but has free tier
        response = requests.get('http://data.fixer.io/api/latest?access_key=YOUR_KEY&base=EUR&symbols=USD', timeout=10)
        # This will fail without API key, but shows the structure
        print("Fixer.io requires API key")
        
    except Exception as e:
        print(f"Error with fixer.io: {e}")

def test_exchangerate_host():
    """Test exchangerate.host (free)"""
    try:
        print("Testing exchangerate.host...")
        response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD', timeout=10)
        data = response.json()
        
        if 'rates' in data and 'USD' in data['rates']:
            eurusd_rate = data['rates']['USD']
            print(f"EUR/USD from exchangerate.host: {eurusd_rate:.4f}")
            return eurusd_rate
        else:
            print("No USD rate in exchangerate.host response")
            
    except Exception as e:
        print(f"Error with exchangerate.host: {e}")
        
    return None

if __name__ == "__main__":
    print("Testing multiple forex APIs for current EUR/USD price...")
    print("Yahoo Finance shows: 1.1744")
    print("-" * 50)
    
    # Test multiple APIs
    exchangerate_price = test_exchangerate_api()
    exchangerate_host_price = test_exchangerate_host()
    test_fixer_api()
    
    print("\nComparison:")
    print(f"Yahoo Finance: 1.1744")
    if exchangerate_price:
        print(f"ExchangeRate-API: {exchangerate_price:.4f}")
    if exchangerate_host_price:
        print(f"ExchangeRate.host: {exchangerate_host_price:.4f}")

#!/usr/bin/env python3
"""
Quick test of real-time forex APIs to fix the price issue
"""

import requests
import json

def test_exchangerate_api() -> float | None:
    """
    Test the free exchangerate API for EUR/USD rate.
    Returns:
        float | None: The EUR/USD rate, or None if unavailable.
    """
    try:
        print("Testing exchangerate-api.com...")
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'rates' in data and 'EUR' in data['rates']:
            eur_rate: float = data['rates']['EUR']
            eurusd_rate: float = 1 / eur_rate  # Convert USD->EUR rate to EUR->USD
            print(f"EUR/USD from exchangerate-api: {eurusd_rate}")
            return eurusd_rate
        else:
            print("No EUR rate in exchangerate-api response")
    except requests.RequestException as e:
        print(f"Network error with exchangerate-api: {e}")
    except Exception as e:
        print(f"Error with exchangerate-api: {e}")
    return None

def test_fixer_api() -> float | None:
    """
    Test fixer.io API (free tier) for EUR/USD rate.
    Returns:
        float | None: The EUR/USD rate, or None if unavailable.
    """
    import os
    try:
        print("Testing fixer.io...")
        api_key: str = os.getenv('FIXER_API_KEY', 'YOUR_KEY')
        if api_key == 'YOUR_KEY':
            print("No API key set for fixer.io. Set FIXER_API_KEY environment variable.")
            return None
        url = f"http://data.fixer.io/api/latest?access_key={api_key}&base=EUR&symbols=USD"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'rates' in data and 'USD' in data['rates']:
            eurusd_rate: float = data['rates']['USD']
            print(f"EUR/USD from fixer.io: {eurusd_rate}")
            return eurusd_rate
        else:
            print("No USD rate in fixer.io response")
    except requests.RequestException as e:
        print(f"Network error with fixer.io: {e}")
    except Exception as e:
        print(f"Error with fixer.io: {e}")
    return None

def test_exchangerate_host() -> float | None:
    """
    Test exchangerate.host (free) for EUR/USD rate.
    Returns:
        float | None: The EUR/USD rate, or None if unavailable.
    """
    try:
        print("Testing exchangerate.host...")
        response = requests.get('https://api.exchangerate.host/latest?base=EUR&symbols=USD', timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'rates' in data and 'USD' in data['rates']:
            eurusd_rate: float = data['rates']['USD']
            print(f"EUR/USD from exchangerate.host: {eurusd_rate}")
            return eurusd_rate
        else:
            print("No USD rate in exchangerate.host response")
    except requests.RequestException as e:
        print(f"Network error with exchangerate.host: {e}")
    except Exception as e:
        print(f"Error with exchangerate.host: {e}")
    return None

if __name__ == "__main__":
    print("Testing multiple forex APIs for current EUR/USD price...")
    print("Yahoo Finance shows: 1.1744")
    print("-" * 50)
    # Test multiple APIs
    exchangerate_price: float | None = test_exchangerate_api()
    exchangerate_host_price: float | None = test_exchangerate_host()
    fixer_price: float | None = test_fixer_api()
    print("\nComparison:")
    print(f"Yahoo Finance: 1.1744")
    if exchangerate_price is not None:
        print(f"ExchangeRate-API: {exchangerate_price}")
    if exchangerate_host_price is not None:
        print(f"ExchangeRate.host: {exchangerate_host_price}")
    if fixer_price is not None:
        print(f"Fixer.io: {fixer_price}")

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

def test_coingecko_api(symbol: str = "bitcoin", vs_currency: str = "usd") -> float | None:
    """
    Test CoinGecko API for crypto price (default: BTC/USD).
    Returns:
        float | None: The price, or None if unavailable.
    """
    try:
        print(f"Testing CoinGecko for {symbol.upper()}/{vs_currency.upper()}...")
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies={vs_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if symbol in data and vs_currency in data[symbol]:
            price: float = data[symbol][vs_currency]
            print(f"{symbol.upper()}/{vs_currency.upper()} from CoinGecko: {price}")
            return price
        else:
            print(f"No {symbol}/{vs_currency} price in CoinGecko response")
    except requests.RequestException as e:
        print(f"Network error with CoinGecko: {e}")
    except Exception as e:
        print(f"Error with CoinGecko: {e}")
    return None

def test_binance_api(symbol: str = "BTCUSDT") -> float | None:
    """
    Test Binance API for crypto price (default: BTC/USDT).
    Returns:
        float | None: The price, or None if unavailable.
    """
    try:
        print(f"Testing Binance for {symbol}...")
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'price' in data:
            price: float = float(data['price'])
            print(f"{symbol} from Binance: {price}")
            return price
        else:
            print(f"No price in Binance response for {symbol}")
    except requests.RequestException as e:
        print(f"Network error with Binance: {e}")
    except Exception as e:
        print(f"Error with Binance: {e}")
    return None

if __name__ == "__main__":
    print("Testing multiple forex and crypto APIs for current prices...")
    print("Forex (EUR/USD): Yahoo Finance shows: 1.1744")
    print("Crypto (BTC/USD): CoinGecko/Binance/Yahoo Finance")
    print("-" * 50)
    # Forex APIs
    exchangerate_price: float | None = test_exchangerate_api()
    exchangerate_host_price: float | None = test_exchangerate_host()
    fixer_price: float | None = test_fixer_api()
    # Crypto APIs
    btc_coingecko: float | None = test_coingecko_api("bitcoin", "usd")
    eth_coingecko: float | None = test_coingecko_api("ethereum", "usd")
    btc_binance: float | None = test_binance_api("BTCUSDT")
    eth_binance: float | None = test_binance_api("ETHUSDT")
    print("\nComparison:")
    print(f"Yahoo Finance (EUR/USD): 1.1744")
    if exchangerate_price is not None:
        print(f"ExchangeRate-API (EUR/USD): {exchangerate_price}")
    if exchangerate_host_price is not None:
        print(f"ExchangeRate.host (EUR/USD): {exchangerate_host_price}")
    if fixer_price is not None:
        print(f"Fixer.io (EUR/USD): {fixer_price}")
    print(f"Yahoo Finance (BTC/USD): 29300.00")
    if btc_coingecko is not None:
        print(f"CoinGecko (BTC/USD): {btc_coingecko}")
    if eth_coingecko is not None:
        print(f"CoinGecko (ETH/USD): {eth_coingecko}")
    if btc_binance is not None:
        print(f"Binance (BTC/USDT): {btc_binance}")
    if eth_binance is not None:
        print(f"Binance (ETH/USDT): {eth_binance}")

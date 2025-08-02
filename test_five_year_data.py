#!/usr/bin/env python3
"""
Test script to verify 5-year historical data fetching
"""
import requests
import time
import json

def test_five_year_data():
    try:
        print("Testing 5-year historical data configuration...")
        
        # Test crypto pair with 5-year data
        print("\n1. Testing BTCUSD with 5-year historical data...")
        start_time = time.time()
        
        r = requests.get("http://localhost:5000/api/forex/data/BTCUSD?period=5y&timeframe=1d", timeout=20)
        end_time = time.time()
        
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                chart_data = data.get('data', [])
                print(f"Historical data points received: {len(chart_data)}")
                if chart_data:
                    print(f"First data point: {chart_data[0]}")
                    print(f"Last data point: {chart_data[-1]}")
                    
                    # Calculate date range
                    if len(chart_data) > 1:
                        first_time = chart_data[0]['timestamp']
                        last_time = chart_data[-1]['timestamp']
                        days_span = (last_time - first_time) / (1000 * 60 * 60 * 24)
                        print(f"Data spans approximately {days_span:.0f} days")
            else:
                print(f"API returned success=false: {data}")
        else:
            print(f"Error: {r.text}")
            
        # Test technical analysis with 5-year data
        print("\n2. Testing technical analysis with 5-year data...")
        start_time = time.time()
        
        r = requests.get("http://localhost:5000/api/technical/BTCUSD?timeframe=1d", timeout=20)
        end_time = time.time()
        
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                print(f"Technical analysis successful")
                trend = data.get('trend', {})
                print(f"Trend direction: {trend.get('direction', 'Unknown')}")
                print(f"Trend strength: {trend.get('strength', 'Unknown')}")
                if 'data_info' in data:
                    print(f"Data info: {data['data_info']}")
            else:
                print(f"Technical analysis failed: {data}")
        else:
            print(f"Technical analysis error: {r.text}")
            
        # Test forex pair as well
        print("\n3. Testing EURUSD with 5-year historical data...")
        start_time = time.time()
        
        r = requests.get("http://localhost:5000/api/forex/data/EURUSD?period=5y&timeframe=1h", timeout=20)
        end_time = time.time()
        
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                chart_data = data.get('data', [])
                print(f"EURUSD historical data points: {len(chart_data)}")
                if chart_data:
                    # Calculate date range
                    if len(chart_data) > 1:
                        first_time = chart_data[0]['timestamp']
                        last_time = chart_data[-1]['timestamp']
                        days_span = (last_time - first_time) / (1000 * 60 * 60 * 24)
                        print(f"EURUSD data spans approximately {days_span:.0f} days")
            else:
                print(f"EURUSD API returned success=false: {data}")
        else:
            print(f"EURUSD Error: {r.text}")
            
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out - server may still have issues")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_five_year_data()

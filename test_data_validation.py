#!/usr/bin/env python3
"""
Test Data Validation System
Tests the comprehensive data validation for forex prices
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.data_validator import ForexDataValidator, validate_forex_data
from datetime import datetime, timedelta
import time

def test_price_validation():
    """Test price validation with various scenarios"""
    print("=" * 60)
    print("FOREX DATA VALIDATION SYSTEM TEST")
    print("=" * 60)
    
    validator = ForexDataValidator()
    
    test_cases = [
        # Valid cases
        {"pair": "EURUSD", "price": 1.0850, "description": "Normal EURUSD price"},
        {"pair": "GBPUSD", "price": 1.2650, "description": "Normal GBPUSD price"},
        {"pair": "USDJPY", "price": 147.50, "description": "Normal USDJPY price"},
        {"pair": "USDCHF", "price": 0.8950, "description": "Normal USDCHF price"},
        
        # Edge cases - still valid but warnings expected
        {"pair": "EURUSD", "price": 1.0000, "description": "EURUSD at parity (edge case)"},
        {"pair": "USDJPY", "price": 160.00, "description": "USDJPY at upper range"},
        
        # Invalid cases
        {"pair": "EURUSD", "price": 2.5000, "description": "EURUSD way too high"},
        {"pair": "EURUSD", "price": 0.5000, "description": "EURUSD way too low"},
        {"pair": "USDJPY", "price": 50.00, "description": "USDJPY too low"},
        {"pair": "USDJPY", "price": 200.00, "description": "USDJPY too high"},
        
        # Format issues
        {"pair": "EURUSD", "price": -1.0850, "description": "Negative price"},
        {"pair": "EURUSD", "price": 0, "description": "Zero price"},
        
        # High precision (warnings expected)
        {"pair": "EURUSD", "price": 1.085012345678, "description": "EURUSD with excessive precision"},
    ]
    
    print("\n1. BASIC PRICE VALIDATION TESTS")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        pair = test_case["pair"]
        price = test_case["price"]
        description = test_case["description"]
        
        print(f"\nTest {i}: {description}")
        print(f"Pair: {pair}, Price: {price}")
        
        result = validate_forex_data(pair, price)
        
        print(f"Valid: {result['is_valid']}")
        print(f"Confidence: {result['confidence_score']}%")
        
        if result['errors']:
            print(f"Errors: {result['errors']}")
        if result['warnings']:
            print(f"Warnings: {result['warnings']}")
    
    print("\n" + "=" * 60)
    print("2. PRICE CHANGE VALIDATION TESTS")
    print("-" * 40)
    
    # Test price change validation
    base_price = 1.0850
    
    # First, establish a baseline
    result1 = validate_forex_data("EURUSD", base_price)
    print(f"\nBaseline: EURUSD = {base_price} (confidence: {result1['confidence_score']}%)")
    
    # Wait a moment to simulate time passage
    time.sleep(0.1)
    
    # Test normal price changes
    price_changes = [
        {"price": 1.0851, "description": "Small increase (+0.0001)"},
        {"price": 1.0840, "description": "Small decrease (-0.0010)"},
        {"price": 1.0900, "description": "Moderate increase (+0.0050)"},
        {"price": 1.0800, "description": "Moderate decrease (-0.0050)"},
        {"price": 1.1500, "description": "Large increase (+0.0650) - should warn"},
        {"price": 1.0000, "description": "Extreme decrease (-0.0850) - should error"},
    ]
    
    for i, change in enumerate(price_changes, 1):
        new_price = change["price"]
        description = change["description"]
        
        print(f"\nChange Test {i}: {description}")
        result = validate_forex_data("EURUSD", new_price)
        
        change_percent = ((new_price - base_price) / base_price) * 100
        print(f"Price: {new_price} ({change_percent:+.2f}%)")
        print(f"Valid: {result['is_valid']}, Confidence: {result['confidence_score']}%")
        
        if result['errors']:
            print(f"Errors: {result['errors']}")
        if result['warnings']:
            print(f"Warnings: {result['warnings']}")
    
    print("\n" + "=" * 60)
    print("3. TIMESTAMP VALIDATION TESTS")
    print("-" * 40)
    
    now = datetime.utcnow()
    timestamp_tests = [
        {"timestamp": now, "description": "Current time"},
        {"timestamp": now - timedelta(minutes=1), "description": "1 minute ago"},
        {"timestamp": now - timedelta(minutes=10), "description": "10 minutes ago (should warn)"},
        {"timestamp": now - timedelta(hours=2), "description": "2 hours ago (should error)"},
        {"timestamp": now + timedelta(minutes=10), "description": "Future timestamp (should error)"},
    ]
    
    for i, test in enumerate(timestamp_tests, 1):
        timestamp = test["timestamp"]
        description = test["description"]
        
        print(f"\nTimestamp Test {i}: {description}")
        result = validate_forex_data("EURUSD", 1.0850, timestamp)
        
        age_seconds = (now - timestamp).total_seconds()
        print(f"Age: {age_seconds:.0f} seconds")
        print(f"Valid: {result['is_valid']}, Confidence: {result['confidence_score']}%")
        
        if result['errors']:
            print(f"Errors: {result['errors']}")
        if result['warnings']:
            print(f"Warnings: {result['warnings']}")
    
    print("\n" + "=" * 60)
    print("4. VALIDATION STATISTICS")
    print("-" * 40)
    
    stats = validator.get_validation_stats()
    print(f"Total validations: {stats['total_validations']}")
    print(f"Valid percentage: {stats['valid_percentage']:.1f}%")
    print(f"Average confidence: {stats['average_confidence_score']:.1f}%")
    print(f"Recent validations (1h): {stats['recent_validations_1h']}")
    
    if stats['last_validation']:
        last = stats['last_validation']
        print(f"Last validation: {last['pair']} = {last['price']} "
              f"(valid: {last['is_valid']}, confidence: {last['confidence_score']}%)")
    
    print("\n" + "=" * 60)
    print("5. MARKET HOURS VALIDATION")
    print("-" * 40)
    
    # Test different times of week
    import calendar
    
    # Saturday evening (market closed)
    saturday = datetime(2025, 7, 26, 22, 0, 0)  # Saturday 10 PM UTC
    result_sat = validate_forex_data("EURUSD", 1.0850, saturday)
    print(f"\nSaturday evening: Valid={result_sat['is_valid']}, "
          f"Confidence={result_sat['confidence_score']}%")
    if result_sat['warnings']:
        print(f"Warnings: {result_sat['warnings']}")
    
    # Monday morning (market open)
    monday = datetime(2025, 7, 28, 8, 0, 0)  # Monday 8 AM UTC (London session)
    result_mon = validate_forex_data("EURUSD", 1.0850, monday)
    print(f"Monday morning: Valid={result_mon['is_valid']}, "
          f"Confidence={result_mon['confidence_score']}%")
    
    print("\n" + "=" * 60)
    print("DATA VALIDATION SYSTEM TEST COMPLETED")
    print("=" * 60)

def test_integration_with_data_fetcher():
    """Test integration with data fetcher"""
    print("\n" + "=" * 60)
    print("INTEGRATION TEST WITH DATA FETCHER")
    print("-" * 40)
    
    try:
        from backend.data_fetcher import DataFetcher
        
        fetcher = DataFetcher()
        
        # Test a few pairs
        test_pairs = ["EURUSD", "GBPUSD", "USDJPY"]
        
        for pair in test_pairs:
            print(f"\nTesting {pair}:")
            
            # Get basic price
            price = fetcher.get_current_price(pair)
            print(f"Raw price: {price}")
            
            if price:
                # Validate it
                validation = validate_forex_data(pair, price)
                print(f"Validation - Valid: {validation['is_valid']}, "
                      f"Confidence: {validation['confidence_score']}%")
                
                if validation['warnings']:
                    print(f"Warnings: {validation['warnings']}")
                if validation['errors']:
                    print(f"Errors: {validation['errors']}")
            
            # Test validated price data method if available
            try:
                validated_data = fetcher.get_validated_price_data(pair)
                print(f"Validated data available: {validated_data['success']}")
                if validated_data['success']:
                    val_info = validated_data['validation']
                    print(f"Data quality: {validated_data['data_quality']} "
                          f"({val_info['confidence_score']}%)")
            except AttributeError:
                print("get_validated_price_data method not available (using older data fetcher)")
    
    except ImportError as e:
        print(f"Could not import data fetcher: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_price_validation()
    test_integration_with_data_fetcher()

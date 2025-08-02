#!/usr/bin/env python3
"""
Direct test of signal generation to see what's happening
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.signal_generator import SignalGenerator
import requests

def test_signal_generation_direct():
    print("Testing signal generation directly...")
    
    # Test the SignalGenerator class directly
    sg = SignalGenerator()
    
    # Mock some technical analysis data
    mock_tech_analysis = {
        'trend_analysis': {'direction': 'Bullish', 'confidence': 60},
        'momentum_indicators': {
            'macd': {'macd': 0.5, 'signal': 0.3},
            'roc': 1.5
        },
        'oscillators': {
            'rsi': {'value': 35},  # Should trigger oversold signal
            'stochastic': {'k': 25}  # Should trigger oversold signal
        }
    }
    
    mock_fund_analysis = {
        'summary': {'overall_bias': 'BULLISH', 'confidence': 65}
    }
    
    try:
        # Test signal generation
        result = sg._calculate_technical_signal(mock_tech_analysis)
        print(f"Technical signal result: {result}")
        
        fund_result = sg._calculate_fundamental_signal(mock_fund_analysis)
        print(f"Fundamental signal result: {fund_result}")
        
    except Exception as e:
        print(f"Error in direct signal generation: {e}")
        
    # Test basic signals function
    print("\nTesting basic signals function...")
    try:
        # Import the function
        from app import generate_basic_signals
        
        # Test for different pairs
        pairs = ['EURUSD', 'GBPUSD', 'USDJPY']
        for pair in pairs:
            signals = generate_basic_signals(pair, 1.1000)
            signal_type = signals['signal']['type']
            confidence = signals['signal']['confidence']
            print(f"{pair}: {signal_type} ({confidence}%)")
            
    except Exception as e:
        print(f"Error testing basic signals: {e}")

if __name__ == "__main__":
    test_signal_generation_direct()

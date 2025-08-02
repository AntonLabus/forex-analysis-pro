#!/usr/bin/env python3
"""
Test the new time-based signal generation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the updated function
from app import generate_basic_signals

def test_hourly_signals():
    print("Testing hourly signal variation...")
    
    pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'EURGBP']
    
    print("Current signals:")
    for pair in pairs:
        signals = generate_basic_signals(pair, 1.1000)
        signal_type = signals['signal']['type']
        confidence = signals['signal']['confidence']
        strength = signals['signal']['strength']
        print(f"{pair}: {signal_type} ({confidence:.1f}%, strength: {strength:.2f})")
    
    # Count distribution
    signal_counts = {'BUY': 0, 'SELL': 0, 'HOLD': 0}
    for pair in pairs:
        signals = generate_basic_signals(pair, 1.1000)
        signal_type = signals['signal']['type']
        signal_counts[signal_type] += 1
    
    print(f"\nSignal distribution:")
    total = sum(signal_counts.values())
    for signal_type, count in signal_counts.items():
        percentage = (count / total) * 100
        print(f"{signal_type}: {count}/{total} ({percentage:.1f}%)")

if __name__ == "__main__":
    test_hourly_signals()

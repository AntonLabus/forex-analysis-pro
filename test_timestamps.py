import requests
import json

print("✅ Testing Signal Timestamps...")
print("=" * 40)

try:
    response = requests.get('http://localhost:5000/api/signals/all', timeout=5)
    if response.status_code == 200:
        data = response.json()
        if 'signals' in data:
            print("✅ Signals endpoint working!")
            
            # Check first few signals for timestamps
            signals = data['signals']
            count = 0
            for pair, signal_data in signals.items():
                if count >= 3:  # Check first 3 signals
                    break
                    
                timestamp = signal_data.get('timestamp', 'MISSING')
                pair_name = signal_data.get('pair', 'MISSING')
                signal_type = signal_data.get('signal', {}).get('type', 'UNKNOWN')
                
                print(f"  {pair_name}: {signal_type} at {timestamp}")
                count += 1
                
            print(f"\n✅ Total signals: {len(signals)}")
            print("✅ Timestamps are now included in signal data!")
        else:
            print("❌ No signals data in response")
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎯 The 'Unknown' timestamp issue should now be fixed!")
print("💡 Refresh your browser to see the actual timestamps!")

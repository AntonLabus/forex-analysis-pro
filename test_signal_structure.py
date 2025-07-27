import requests
import json

print("Testing Signal Data Structure...")
print("=" * 40)

try:
    # Test signals endpoint
    response = requests.get('http://localhost:5000/api/signals', timeout=10)
    if response.status_code == 200:
        data = response.json()
        print("✅ Signals endpoint responding")
        print(f"Response structure: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        if 'data' in data and data['data']:
            signal = data['data'][0]
            print(f"\nFirst signal structure:")
            print(f"  Keys: {list(signal.keys())}")
            print(f"  Pair: {signal.get('pair', 'MISSING')}")
            print(f"  Timestamp: {signal.get('timestamp', 'MISSING')}")
            print(f"  Timestamp type: {type(signal.get('timestamp'))}")
            
            if 'signal' in signal:
                print(f"  Signal data: {signal['signal']}")
        else:
            print("❌ No signal data in response")
            print(f"Full response: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Signals endpoint error: {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")

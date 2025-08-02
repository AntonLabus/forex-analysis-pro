import requests
import json

# Check signal details for EURUSD
r = requests.get('http://localhost:5000/api/signals/EURUSD?timeframe=1h')
if r.status_code == 200:
    data = r.json()
    print('EURUSD Signal Data:')
    print(f'Success: {data.get("success")}')
    if data.get('signal'):
        signal = data['signal']['signal']
        print(f'Direction: {signal.get("direction")}')
        print(f'Confidence: {signal.get("confidence")}')
        print(f'Raw signal: {signal.get("raw_signal")}')
        print(f'Components: {signal.get("components")}')
        print(f'Strength: {signal.get("strength")}')
        
        # Show technical details
        if 'technical' in data['signal']:
            tech = data['signal']['technical']
            print(f'\nTechnical Analysis:')
            print(json.dumps(tech, indent=2))
else:
    print(f'Error: {r.status_code} - {r.text}')

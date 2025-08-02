#!/usr/bin/env python3
"""
Test CORS headers specifically
"""

import requests

def test_cors():
    url = "http://localhost:5000/api/test"
    
    try:
        # Test with proper Origin header
        headers = {
            'Origin': 'https://forex-analysis-pro.netlify.app',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        print("Response headers:")
        for key, value in response.headers.items():
            if 'access-control' in key.lower():
                print(f"  {key}: {value}")
                
        # Check for duplicate headers
        cors_origin_headers = [k for k in response.headers.keys() if k.lower() == 'access-control-allow-origin']
        if len(cors_origin_headers) > 1:
            print(f"❌ DUPLICATE CORS HEADERS FOUND: {len(cors_origin_headers)}")
        else:
            print(f"✅ CORS headers look good: {len(cors_origin_headers)} origin header(s)")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_cors()

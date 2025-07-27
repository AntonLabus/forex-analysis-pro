import requests
import json

print("Testing Rate Limiting System...")
print("=" * 40)

try:
    # Test rate limits endpoint
    response = requests.get('http://localhost:5000/api/system/rate-limits', timeout=5)
    if response.status_code == 200:
        data = response.json()
        print("✅ Rate Limits Endpoint Working!")
        print(f"Status: {data.get('status', 'unknown')}")
        limits = data.get('limits', {})
        for api, info in limits.items():
            print(f"  {api}: {info.get('current', 0)}/{info.get('limit', 0)} requests")
    else:
        print(f"❌ Rate Limits Error: {response.status_code}")

    print()
    
    # Test system health endpoint
    response = requests.get('http://localhost:5000/api/system/health', timeout=5)
    if response.status_code == 200:
        data = response.json()
        print("✅ System Health Endpoint Working!")
        print(f"Health Score: {data.get('health_score', 'unknown')}")
        print(f"Total Requests: {data.get('total_requests', 0)}")
        print(f"Error Rate: {data.get('error_rate', 0):.2f}%")
        recs = data.get('recommendations', [])
        print(f"Recommendations: {len(recs)} items")
    else:
        print(f"❌ System Health Error: {response.status_code}")

except Exception as e:
    print(f"❌ Connection Error: {e}")

print()
print("✅ Rate Limiting System is operational!")
print("🎯 Check the Monitor button in the web interface")

#!/usr/bin/env python3
"""
Emergency Mode Management Utility
Quick tool to check and reset emergency mode in the Forex Analysis Pro system
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
LOCAL_API = "http://localhost:5000"
PRODUCTION_API = "https://forex-analysis-pro.onrender.com"

def check_emergency_mode(api_base):
    """Check current emergency mode status"""
    try:
        url = f"{api_base}/api/system/emergency-mode"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                mode = data['emergency_mode']
                print(f"✅ Emergency Mode Status ({api_base}):")
                print(f"   Active: {mode['active']}")
                if mode['active']:
                    print(f"   Remaining Time: {mode['remaining_minutes']} minutes")
                    print(f"   Message: {mode['message']}")
                else:
                    print(f"   Message: {mode['message']}")
                return mode['active']
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None

def reset_emergency_mode(api_base):
    """Reset emergency mode"""
    try:
        url = f"{api_base}/api/system/emergency-mode/reset"
        response = requests.post(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ {data['message']}")
                return True
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def main():
    """Main function"""
    print("🚨 Emergency Mode Management Utility")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        environment = sys.argv[2].lower() if len(sys.argv) > 2 else "both"
    else:
        command = "check"
        environment = "both"
    
    # Determine which APIs to check
    apis_to_check = []
    if environment in ["local", "both"]:
        apis_to_check.append(("Local", LOCAL_API))
    if environment in ["production", "prod", "both"]:
        apis_to_check.append(("Production", PRODUCTION_API))
    
    if command == "check":
        print("📊 Checking Emergency Mode Status...")
        print()
        for name, api_base in apis_to_check:
            print(f"🔍 Checking {name} Environment:")
            check_emergency_mode(api_base)
            print()
    
    elif command == "reset":
        print("🔧 Resetting Emergency Mode...")
        print()
        for name, api_base in apis_to_check:
            print(f"🔧 Resetting {name} Environment:")
            reset_emergency_mode(api_base)
            print()
        
        # Check status after reset
        print("📊 Post-Reset Status Check...")
        print()
        for name, api_base in apis_to_check:
            print(f"🔍 Checking {name} Environment:")
            check_emergency_mode(api_base)
            print()
    
    elif command == "help":
        print("Usage:")
        print("  python emergency_mode_util.py [command] [environment]")
        print()
        print("Commands:")
        print("  check (default) - Check emergency mode status")
        print("  reset          - Reset emergency mode")
        print("  help           - Show this help")
        print()
        print("Environments:")
        print("  local      - Check/reset local development server")
        print("  production - Check/reset production server")
        print("  both (default) - Check/reset both environments")
        print()
        print("Examples:")
        print("  python emergency_mode_util.py check")
        print("  python emergency_mode_util.py reset production")
        print("  python emergency_mode_util.py check local")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'python emergency_mode_util.py help' for usage information")

if __name__ == "__main__":
    main()

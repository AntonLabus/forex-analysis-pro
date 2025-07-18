#!/usr/bin/env python3
"""
Forex Analysis Pro - Startup Script
Cross-platform startup script with dependency checking and installation
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_package_installed(package_name):
    """Check if a Python package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_requirements():
    """Install requirements from requirements.txt"""
    if not os.path.exists('requirements.txt'):
        print("ERROR: requirements.txt not found")
        return False
    
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        return False

def setup_database():
    """Create database if it doesn't exist"""
    if not os.path.exists('forex_analysis.db'):
        print("Creating database...")
        try:
            from backend.database import Database
            db = Database()
            db.init_db()
            print("Database created successfully!")
        except Exception as e:
            print(f"ERROR: Failed to create database: {e}")
            return False
    else:
        print("Database already exists.")
    return True

def start_application():
    """Start the Flask application"""
    print("\n" + "="*60)
    print("         Forex Analysis Pro - Starting Server")
    print("="*60)
    print("\nThe application will be available at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("\n" + "="*60 + "\n")
    
    try:
        import app
        app.app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except Exception as e:
        print(f"\nERROR: Failed to start application: {e}")
        return False
    return True

def main():
    """Main startup function"""
    print("\n" + "="*60)
    print("         Forex Analysis Pro - Startup Script")
    print("="*60 + "\n")
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    print("Python version check passed.")
    
    # Check if Flask is installed (key dependency)
    if not check_package_installed('flask'):
        print("Key dependencies not found. Installing...")
        if not install_requirements():
            input("Press Enter to exit...")
            return
    else:
        print("Dependencies already installed.")
    
    # Setup database
    if not setup_database():
        input("Press Enter to exit...")
        return
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()

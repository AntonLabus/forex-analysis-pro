#!/usr/bin/env python3
"""
Quick test script to verify the Forex Analysis Pro setup
"""

import sys
import os

def test_python_version():
    """Test Python version compatibility"""
    print(f"✓ Python version: {sys.version}")
    if sys.version_info >= (3, 8):
        print("✓ Python version is compatible")
        return True
    else:
        print("✗ Python 3.8+ required")
        return False

def test_imports():
    """Test critical imports"""
    try:
        import flask
        print(f"✓ Flask {flask.__version__} available")
        
        import pandas
        print(f"✓ Pandas {pandas.__version__} available")
        
        import numpy
        print(f"✓ NumPy {numpy.__version__} available")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'app.py',
        'backend/database.py',
        'backend/data_fetcher.py',
        'backend/technical_analysis.py',
        'backend/fundamental_analysis.py',
        'backend/signal_generator.py',
        'frontend/templates/index.html',
        'frontend/static/css/styles.css',
        'frontend/static/js/app.js',
        'frontend/static/js/chart.js',
        'frontend/static/js/signals.js',
        'frontend/static/js/utils.js',
        'frontend/static/js/config.js',
        'requirements.txt',
        'README.md'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - Missing!")
            all_files_exist = False
    
    return all_files_exist

def main():
    """Run all tests"""
    print("="*60)
    print("    Forex Analysis Pro - Setup Verification")
    print("="*60)
    print()
    
    # Test Python version
    print("Testing Python version...")
    python_ok = test_python_version()
    print()
    
    # Test imports
    print("Testing Python dependencies...")
    imports_ok = test_imports()
    print()
    
    # Test file structure
    print("Testing file structure...")
    files_ok = test_file_structure()
    print()
    
    # Summary
    print("="*60)
    print("Summary:")
    print(f"Python version: {'✓' if python_ok else '✗'}")
    print(f"Dependencies: {'✓' if imports_ok else '✗'}")
    print(f"File structure: {'✓' if files_ok else '✗'}")
    print()
    
    if python_ok and imports_ok and files_ok:
        print("🎉 Setup verification PASSED!")
        print("You can now run the application with:")
        print("   python start.py")
        print("   OR")
        print("   python app.py")
        print()
        print("The application will be available at: http://localhost:5000")
    else:
        print("❌ Setup verification FAILED!")
        if not imports_ok:
            print("Run: pip install -r requirements.txt")
    
    print("="*60)

if __name__ == "__main__":
    main()

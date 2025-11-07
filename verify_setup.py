#!/usr/bin/env python3
"""
Quick setup verification script for Smart Patient Health Assistant
Run this after installation to verify everything is configured correctly.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version >= (3, 9):
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (3.9+ required)")
        return False

def check_dependencies():
    """Check if key dependencies are installed"""
    print("\n📦 Checking dependencies...")
    required = {
        'flask': 'Flask',
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'requests': 'Requests',
        'yaml': 'PyYAML'
    }
    
    all_ok = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} not installed")
            all_ok = False
    
    return all_ok

def check_config_files():
    """Check if configuration files exist"""
    print("\n⚙️  Checking configuration...")
    
    checks = []
    
    # Check for .env file
    if Path('.env').exists():
        print("   ✅ .env file exists")
        checks.append(True)
    else:
        print("   ⚠️  .env file not found (copy from .env.example)")
        checks.append(False)
    
    # Check for config.yaml
    if Path('config/config.yaml').exists():
        print("   ✅ config/config.yaml exists")
        checks.append(True)
    elif Path('config/config.yaml.template').exists():
        print("   ⚠️  config.yaml not found (copy from config.yaml.template)")
        checks.append(False)
    else:
        print("   ❌ No config files found")
        checks.append(False)
    
    return all(checks)

def check_models():
    """Check if ML models exist"""
    print("\n🤖 Checking ML models...")
    
    models = [
        'models/saved_models/diabetes_model.joblib',
        'models/saved_models/heart_model.joblib',
        'models/saved_models/kidney_model.joblib'
    ]
    
    all_ok = True
    for model in models:
        if Path(model).exists():
            print(f"   ✅ {Path(model).name}")
        else:
            print(f"   ❌ {Path(model).name} not found")
            all_ok = False
    
    return all_ok

def check_data():
    """Check if training data exists"""
    print("\n📊 Checking training data...")
    
    datasets = [
        'data/raw/diabetes.csv',
        'data/raw/heart.csv',
        'data/raw/kidney.csv'
    ]
    
    all_ok = True
    for dataset in datasets:
        if Path(dataset).exists():
            print(f"   ✅ {Path(dataset).name}")
        else:
            print(f"   ⚠️  {Path(dataset).name} not found")
            all_ok = False
    
    return all_ok

def test_api_import():
    """Test if API can be imported"""
    print("\n🔌 Testing API import...")
    try:
        sys.path.insert(0, os.path.abspath('.'))
        from src.api.app import app
        print("   ✅ Flask API imports successfully")
        return True
    except Exception as e:
        print(f"   ❌ API import failed: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("Smart Patient Health Assistant - Setup Verification")
    print("=" * 60)
    
    results = [
        check_python_version(),
        check_dependencies(),
        check_config_files(),
        check_models(),
        check_data(),
        test_api_import()
    ]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All checks passed! You're ready to run the application.")
        print("\nNext steps:")
        print("1. Start Flask API:    python -m src.api.app")
        print("2. Start Streamlit:    streamlit run app.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nSetup instructions:")
        print("1. Install dependencies:  pip install -r requirements.txt")
        print("2. Copy .env.example to .env and configure")
        print("3. Copy config.yaml.template to config.yaml")
    print("=" * 60)
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())

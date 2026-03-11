#!/usr/bin/env python3
"""
AI Invoice Parser System Check
Verifies installation and configuration
"""

import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("📍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_package(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        print(f"   ✅ {package_name}")
        return True
    else:
        print(f"   ❌ {package_name} (Missing)")
        return False

def check_packages():
    """Check all required packages"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "pdfplumber",
        "pandas",
        "docx",
        "PIL",
        "google.generativeai",
        "dotenv"
    ]
    
    all_installed = True
    for package in required_packages:
        if not check_package(package):
            all_installed = False
    
    return all_installed

def check_env_file():
    """Check environment configuration"""
    print("\n⚙️  Checking environment configuration...")
    
    if os.path.exists('.env'):
        print("   ✅ .env file found")
        
        with open('.env', 'r') as f:
            content = f.read()
            
        if 'GEMINI_API_KEY=your_gemini_api_key_here' in content:
            print("   ⚠️  Gemini API key not configured")
            print("      Edit .env and set your API key for AI features")
            return False
        elif 'GEMINI_API_KEY=' in content:
            print("   ✅ Gemini API key configured")
            return True
        else:
            print("   ⚠️  Gemini API key line not found in .env")
            return False
    else:
        print("   ❌ .env file missing")
        return False

def check_directories():
    """Check required directories exist"""
    print("\n📁 Checking directory structure...")
    
    dirs = ['backend', 'frontend', 'temp', 'sample_files']
    all_exist = True
    
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ (Missing)")
            all_exist = False
    
    return all_exist

def check_files():
    """Check key files exist"""
    print("\n📄 Checking key files...")
    
    files = [
        'backend/app.py',
        'backend/extractor.py', 
        'backend/config.py',
        'frontend/index.html',
        'frontend/script.js',
        'frontend/style.css',
        'requirements.txt'
    ]
    
    all_exist = True
    for file_name in files:
        if os.path.exists(file_name):
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ {file_name} (Missing)")
            all_exist = False
    
    return all_exist

def main():
    """Run all system checks"""
    print("🤖 AI Invoice Parser System Check")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_packages(), 
        check_env_file(),
        check_directories(),
        check_files()
    ]
    
    print("\n" + "=" * 50)
    print("📊 SYSTEM STATUS")
    print("=" * 50)
    
    if all(checks):
        print("🎉 ALL CHECKS PASSED!")
        print("\n✅ System ready for AI-powered invoice processing")
        print("\n🚀 Next steps:")
        print("   1. Run: start_backend.bat (Windows) or uvicorn app:app --reload")
        print("   2. Open: frontend/index.html in your browser")
        print("   3. Test with sample files from sample_files/ directory")
    else:
        print("⚠️  SOME ISSUES FOUND")
        print("\n❌ Please fix the issues above before proceeding")
        print("\n🔧 Common fixes:")
        print("   • Install missing packages: pip install -r requirements.txt")
        print("   • Configure Gemini API: Edit .env file with your API key")
        print("   • Check file permissions and directory structure")
    
    print("\n📚 For detailed setup help, see AI_SETUP.md")

if __name__ == "__main__":
    main()
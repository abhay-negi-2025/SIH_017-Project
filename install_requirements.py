#!/usr/bin/env python
"""
Smart requirements installer for Alumni Connect Platform
This script handles common installation issues and provides fallback options
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def install_package(package, description):
    """Install a single package with error handling"""
    print(f"🔄 Installing {description}...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              check=True, capture_output=True, text=True)
        print(f"✅ {description} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {description}")
        print(f"Error: {e.stderr}")
        return False

def install_requirements():
    """Install requirements with fallback options"""
    print("🚀 Installing Alumni Connect Platform Requirements")
    print("=" * 60)
    
    # Try installing from main requirements file first
    if os.path.exists("requirements.txt"):
        print("\n📦 Attempting to install from requirements.txt...")
        if run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Installing main requirements"):
            print("✅ All requirements installed successfully!")
            return True
        else:
            print("⚠️  Main requirements failed, trying alternative approach...")
    
    # Try installing from minimal requirements
    if os.path.exists("requirements-minimal.txt"):
        print("\n📦 Attempting to install from requirements-minimal.txt...")
        if run_command(f"{sys.executable} -m pip install -r requirements-minimal.txt", 
                      "Installing minimal requirements"):
            print("✅ Minimal requirements installed successfully!")
            return True
        else:
            print("⚠️  Minimal requirements failed, trying individual packages...")
    
    # Install packages individually with fallbacks
    print("\n📦 Installing packages individually...")
    
    packages = [
        ("Django==4.2.7", "Django Framework"),
        ("Pillow>=10.0.0", "Pillow (Image Processing)"),
        ("python-decouple>=3.0", "Environment Variables"),
        ("requests>=2.25.0", "HTTP Requests"),
        ("stripe>=6.0.0", "Stripe Payment Gateway")
    ]
    
    failed_packages = []
    
    for package, description in packages:
        if not install_package(package, description):
            # Try with more flexible version
            flexible_package = package.split("==")[0]
            print(f"🔄 Trying flexible version: {flexible_package}")
            if not install_package(flexible_package, f"{description} (flexible)"):
                failed_packages.append(package)
                print(f"⚠️  Skipping {description} - will use alternatives")
    
    # Handle failed packages
    if failed_packages:
        print(f"\n⚠️  Some packages failed to install: {failed_packages}")
        print("The application will still work with reduced functionality.")
    
    # Install common alternatives
    print("\n🔄 Installing common alternatives...")
    
    alternatives = [
        ("django-environ", "Environment Variables Alternative"),
        ("Pillow-SIMD", "Pillow Alternative (if available)")
    ]
    
    for package, description in alternatives:
        install_package(package, description)
    
    return True

def check_installation():
    """Check if critical packages are installed"""
    print("\n🔍 Checking installation...")
    
    critical_packages = ["django", "PIL", "requests"]
    missing_packages = []
    
    for package in critical_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n⚠️  Missing critical packages: {missing_packages}")
        print("Please install them manually or try the installation again.")
        return False
    else:
        print("\n🎉 All critical packages are available!")
        return True

def main():
    """Main installation function"""
    print("Alumni Connect Platform - Smart Requirements Installer")
    print("=" * 60)
    
    # Upgrade pip first
    print("🔄 Upgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    if install_requirements():
        if check_installation():
            print("\n🎉 Installation completed successfully!")
            print("\n📋 Next steps:")
            print("1. Run: python manage.py migrate")
            print("2. Run: python manage.py createsuperuser")
            print("3. Run: python manage.py runserver")
            print("4. Visit: http://127.0.0.1:8000/")
        else:
            print("\n⚠️  Installation completed with some issues.")
            print("The application may have reduced functionality.")
    else:
        print("\n❌ Installation failed.")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure you have Python 3.8 or higher")
        print("2. Try running: pip install --upgrade pip")
        print("3. Try running: pip install --user -r requirements-minimal.txt")
        print("4. For Windows users, install Visual Studio Build Tools")
        print("5. For macOS users, install Xcode Command Line Tools")

if __name__ == "__main__":
    main()

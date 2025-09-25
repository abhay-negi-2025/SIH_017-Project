#!/usr/bin/env python
"""
Setup script for Alumni Connect Platform
This script helps set up the project for first-time users.
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_environment():
    """Set up the development environment"""
    print("🚀 Setting up Alumni Connect Platform...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies with fallback options
    print("📦 Installing dependencies...")
    
    # Try main requirements first
    if not run_command("pip install -r requirements.txt", "Installing main requirements"):
        print("⚠️  Main requirements failed, trying minimal requirements...")
        
        # Try minimal requirements
        if not run_command("pip install -r requirements-minimal.txt", "Installing minimal requirements"):
            print("⚠️  Minimal requirements failed, trying individual packages...")
            
            # Install critical packages individually
            critical_packages = [
                "Django==4.2.7",
                "Pillow",
                "python-decouple", 
                "requests"
            ]
            
            failed_packages = []
            for package in critical_packages:
                if not run_command(f"pip install {package}", f"Installing {package}"):
                    failed_packages.append(package)
            
            if failed_packages:
                print(f"⚠️  Some packages failed: {failed_packages}")
                print("The application will work with reduced functionality.")
            
            # Try installing just Django as fallback
            if not run_command("pip install Django", "Installing Django (minimum)"):
                print("❌ Even basic Django installation failed.")
                print("Please check your Python environment and try manual installation.")
                sys.exit(1)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_platform.settings')
    
    # Initialize Django
    django.setup()
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        print("⚠️  Migration creation failed, but continuing...")
    
    if not run_command("python manage.py migrate", "Applying database migrations"):
        print("❌ Database migration failed")
        sys.exit(1)
    
    # Create superuser
    print("\n👤 Creating superuser account...")
    print("Please provide the following information for the admin account:")
    
    try:
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created successfully")
    except Exception as e:
        print(f"⚠️  Superuser creation failed: {e}")
        print("You can create it later using: python manage.py createsuperuser")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy env_example.txt to .env and configure your settings")
    print("2. Run the server: python manage.py runserver")
    print("3. Visit: http://127.0.0.1:8000/")
    print("4. Login with your superuser account")
    print("\n📚 For more information, check the README.md file")

if __name__ == '__main__':
    setup_environment()

# Troubleshooting Guide - Alumni Connect Platform

## Common Installation Issues and Solutions

### 1. Wheel Building Errors

**Error**: `Getting requirements to build wheel did not run successfully`

**Solutions**:

#### Option A: Use the Smart Installer
```bash
python install_requirements.py
```

#### Option B: Install Minimal Requirements
```bash
pip install -r requirements-minimal.txt
```

#### Option C: Install Packages Individually
```bash
pip install Django==4.2.7
pip install Pillow
pip install python-decouple
pip install requests
pip install stripe
```

#### Option D: Use Alternative Package Sources
```bash
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

### 2. MySQL Client Issues (Windows)

**Error**: `Microsoft Visual C++ 14.0 is required`

**Solutions**:
- Install Visual Studio Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or use SQLite (default) instead of MySQL
- Or use pre-compiled wheels: `pip install mysqlclient-2.2.0-cp39-cp39-win_amd64.whl`

### 3. Pillow Installation Issues

**Error**: `Could not build wheels for Pillow`

**Solutions**:
```bash
# Try installing system dependencies first
# Ubuntu/Debian:
sudo apt-get install libjpeg-dev zlib1g-dev

# macOS:
brew install libjpeg zlib

# Then install Pillow
pip install Pillow
```

### 4. Python Version Issues

**Error**: `Python 3.8+ required`

**Solutions**:
- Install Python 3.8 or higher
- Use pyenv to manage Python versions
- Create a virtual environment with the correct Python version

### 5. Virtual Environment Issues

**Error**: `Command not found` or permission errors

**Solutions**:
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements-minimal.txt
```

### 6. Django Migration Issues

**Error**: `No module named 'main_app'`

**Solutions**:
```bash
# Make sure you're in the project directory
cd Alumni_Connect_Platform

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6.1. Createsuperuser Password Input Issues

**Error**: Cannot enter password or password input not working

**Solutions**:

#### Option A: Use the Admin Creation Script (Recommended)
```bash
python create_admin.py
```

#### Option B: Use Quick Setup Script
```bash
python quick_setup.py
```

#### Option C: Manual Admin Creation
```python
# Run this in Django shell
python manage.py shell

# Then run these commands:
from django.contrib.auth.models import User
user = User.objects.create_user('admin', 'admin@college.edu', 'admin123')
user.is_staff = True
user.is_superuser = True
user.save()
exit()
```

#### Option D: Environment Variables Method
```bash
# Set environment variables and run createsuperuser
set DJANGO_SUPERUSER_USERNAME=admin
set DJANGO_SUPERUSER_EMAIL=admin@college.edu
set DJANGO_SUPERUSER_PASSWORD=admin123
python manage.py createsuperuser --noinput
```

#### Option E: Use Different Terminal
- Try using Command Prompt instead of PowerShell
- Try using Git Bash or WSL on Windows
- Try using a different terminal application

### 7. Static Files Issues

**Error**: `Static files not found`

**Solutions**:
```bash
# Collect static files
python manage.py collectstatic

# Or run in development mode
python manage.py runserver --insecure
```

### 8. Database Issues

**Error**: `Database is locked` or `Table doesn't exist`

**Solutions**:
```bash
# Delete existing database
rm db.sqlite3

# Run migrations again
python manage.py migrate

# Create demo data
python create_demo_data.py
```

### 9. Port Already in Use

**Error**: `Port 8000 is already in use`

**Solutions**:
```bash
# Use a different port
python manage.py runserver 8001

# Or kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill
```

### 10. Stripe Payment Issues

**Error**: `Stripe API key not found`

**Solutions**:
1. Copy `env_example.txt` to `.env`
2. Add your Stripe keys to `.env` file
3. Or comment out Stripe in requirements if not needed

## Quick Fix Commands

### Complete Reset
```bash
# Remove virtual environment
rm -rf venv

# Create new virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
python install_requirements.py

# Setup database
python manage.py migrate
python manage.py createsuperuser
python create_demo_data.py

# Run server
python manage.py runserver
```

### Minimal Setup (No Dependencies)
```bash
# Install only Django
pip install Django

# Run with SQLite (default)
python manage.py migrate
python manage.py runserver
```

## Platform-Specific Solutions

### Windows
1. Install Visual Studio Build Tools
2. Use Command Prompt as Administrator
3. Install Windows Subsystem for Linux (WSL) if needed

### macOS
1. Install Xcode Command Line Tools: `xcode-select --install`
2. Use Homebrew for system dependencies
3. Consider using pyenv for Python version management

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-dev python3-pip python3-venv
sudo apt-get install libjpeg-dev zlib1g-dev libpq-dev

# Install requirements
pip3 install -r requirements-minimal.txt
```

## Getting Help

If you're still having issues:

1. **Check Python Version**: `python --version` (should be 3.8+)
2. **Check Pip Version**: `pip --version`
3. **Try Virtual Environment**: Create a fresh virtual environment
4. **Use Minimal Requirements**: Install only essential packages
5. **Check System Dependencies**: Install required system libraries

## Demo Mode

If you can't install all dependencies, you can still run the basic application:

```bash
# Install only Django
pip install Django

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

The application will work with basic functionality, though some features like image uploads and payments may be limited.

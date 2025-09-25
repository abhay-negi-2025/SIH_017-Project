#!/bin/bash

echo "========================================"
echo "Alumni Connect Platform - Quick Install"
echo "========================================"
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

python3 --version

echo
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo
echo "Installing requirements..."
python3 install_requirements.py

echo
echo "Setting up database..."
python3 manage.py migrate

echo
echo "Creating demo data..."
python3 create_demo_data.py

echo
echo "========================================"
echo "Installation completed!"
echo "========================================"
echo
echo "To start the server, run:"
echo "python3 manage.py runserver"
echo
echo "Then visit: http://127.0.0.1:8000/"
echo
echo "Demo accounts:"
echo "Admin: username=admin, password=admin123"
echo "Alumni: username=john.doe, password=password123"
echo "Student: username=alice.wilson, password=password123"
echo

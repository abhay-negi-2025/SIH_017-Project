@echo off
echo ========================================
echo Alumni Connect Platform - Quick Install
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing requirements...
python install_requirements.py

echo.
echo Setting up database...
python manage.py migrate

echo.
echo Creating demo data...
python create_demo_data.py

echo.
echo ========================================
echo Installation completed!
echo ========================================
echo.
echo To start the server, run:
echo python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000/
echo.
echo Demo accounts:
echo Admin: username=admin, password=admin123
echo Alumni: username=john.doe, password=password123
echo Student: username=alice.wilson, password=password123
echo.
pause

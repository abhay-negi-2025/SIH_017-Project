@echo off
echo ========================================
echo Fixing Admin User Creation Issue
echo ========================================
echo.

echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Creating admin user (bypassing password input issue)...
python create_admin.py

echo.
echo Setup completed!
echo.
echo Admin credentials:
echo Username: admin
echo Password: admin123
echo.
echo To start the server:
echo python manage.py runserver
echo.
pause

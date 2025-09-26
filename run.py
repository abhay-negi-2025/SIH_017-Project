#!/usr/bin/env python
"""
Simple script to run the Django development server with default settings.
This is useful for quick testing and demonstration purposes.
"""

import os
import sys
import django  # pyright: ignore[reportMissingImports]
from django.core.management import execute_from_command_line  # pyright: ignore[reportMissingImports]

if __name__ == '__main__':
    # Set default settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_platform.settings')
    
    # Initialize Django
    django.setup()
    
    # Run the development server
    print("Starting Alumni Connect Platform...")
    print("Server will be available at: http://127.0.0.1:8000/")
    print("Press Ctrl+C to stop the server")
    
    try:
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

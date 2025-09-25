#!/usr/bin/env python
"""
Quick setup script that handles all the common issues
including the createsuperuser password input problem
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_platform.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import execute_from_command_line
from main_app.models import Profile, CollegeAdmin, Alumni, Student

def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Database migrations completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def create_admin_user():
    """Create admin user without interactive input"""
    print("🔧 Creating admin user...")
    
    username = 'admin'
    email = 'admin@college.edu'
    password = 'admin123'
    
    # Check if admin already exists
    if User.objects.filter(username=username).exists():
        print(f"✅ Admin user '{username}' already exists")
        return True
    
    try:
        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='College',
            last_name='Administrator',
            is_staff=True,
            is_superuser=True
        )
        
        # Create profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'user_type': 'admin'}
        )
        
        # Create college admin profile
        college_admin, created = CollegeAdmin.objects.get_or_create(
            profile=profile,
            defaults={
                'college_name': 'Demo Engineering College',
                'college_id': 'DEMO001',
                'designation': 'Principal'
            }
        )
        
        print("✅ Admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

def create_demo_users():
    """Create demo users for testing"""
    print("👥 Creating demo users...")
    
    # Demo alumni
    alumni_data = [
        {
            'username': 'john.doe',
            'email': 'john.doe@email.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'branch': 'CSE',
            'batch_year': 2018,
            'cgpa': 8.5,
            'current_company': 'Google',
            'current_position': 'Software Engineer',
            'work_experience': 5,
            'is_mentor': True
        },
        {
            'username': 'jane.smith',
            'email': 'jane.smith@email.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'branch': 'ECE',
            'batch_year': 2019,
            'cgpa': 9.0,
            'current_company': 'Microsoft',
            'current_position': 'Product Manager',
            'work_experience': 4,
            'is_mentor': True
        }
    ]
    
    for data in alumni_data:
        if not User.objects.filter(username=data['username']).exists():
            try:
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='password123',
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )
                
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'user_type': 'alumni'}
                )
                
                Alumni.objects.get_or_create(
                    profile=profile,
                    defaults={
                        'batch_year': data['batch_year'],
                        'branch': data['branch'],
                        'cgpa': data['cgpa'],
                        'current_company': data['current_company'],
                        'current_position': data['current_position'],
                        'work_experience': data['work_experience'],
                        'is_mentor': data['is_mentor']
                    }
                )
                print(f"✅ Alumni {data['first_name']} {data['last_name']} created")
            except Exception as e:
                print(f"⚠️  Error creating alumni {data['first_name']}: {e}")
    
    # Demo student
    student_data = {
        'username': 'alice.wilson',
        'email': 'alice.wilson@student.edu',
        'first_name': 'Alice',
        'last_name': 'Wilson',
        'branch': 'CSE',
        'batch_year': 2022,
        'current_semester': 6,
        'cgpa': 8.2,
        'college_name': 'Demo Engineering College'
    }
    
    if not User.objects.filter(username=student_data['username']).exists():
        try:
            user = User.objects.create_user(
                username=student_data['username'],
                email=student_data['email'],
                password='password123',
                first_name=student_data['first_name'],
                last_name=student_data['last_name']
            )
            
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={'user_type': 'student'}
            )
            
            Student.objects.get_or_create(
                profile=profile,
                defaults={
                    'batch_year': student_data['batch_year'],
                    'branch': student_data['branch'],
                    'current_semester': student_data['current_semester'],
                    'cgpa': student_data['cgpa'],
                    'college_name': student_data['college_name']
                }
            )
            print(f"✅ Student {student_data['first_name']} {student_data['last_name']} created")
        except Exception as e:
            print(f"⚠️  Error creating student {student_data['first_name']}: {e}")

def collect_static_files():
    """Collect static files"""
    print("🔄 Collecting static files...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Static files collection failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Alumni Connect Platform - Quick Setup")
    print("=" * 50)
    
    # Run migrations
    if not run_migrations():
        print("❌ Setup failed at migrations stage")
        return False
    
    # Create admin user
    if not create_admin_user():
        print("❌ Setup failed at admin user creation")
        return False
    
    # Create demo users
    create_demo_users()
    
    # Collect static files
    collect_static_files()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Login Credentials:")
    print("👨‍💼 Admin: username='admin', password='admin123'")
    print("👨‍🎓 Alumni: username='john.doe', password='password123'")
    print("👩‍🎓 Alumni: username='jane.smith', password='password123'")
    print("👩‍🎓 Student: username='alice.wilson', password='password123'")
    
    print("\n🚀 To start the server:")
    print("python manage.py runserver")
    print("\n🌐 Then visit: http://127.0.0.1:8000/")
    
    return True

if __name__ == '__main__':
    main()

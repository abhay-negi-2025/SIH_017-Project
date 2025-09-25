#!/usr/bin/env python
"""
Script to create demo data for the Alumni Connect Platform
Run this script after setting up the database to populate it with sample data
"""

import os
import sys
import django
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_platform.settings')
django.setup()

from main_app.models import (
    Profile, Alumni, Student, CollegeAdmin, Event, EventRegistration,
    Mentorship, Internship, Donation
)

def create_demo_users():
    """Create demo users for testing"""
    print("Creating demo users...")
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@college.edu',
            'first_name': 'College',
            'last_name': 'Administrator',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        
        admin_profile, _ = Profile.objects.get_or_create(
            user=admin_user,
            defaults={'user_type': 'admin'}
        )
        
        CollegeAdmin.objects.get_or_create(
            profile=admin_profile,
            defaults={
                'college_name': 'Demo Engineering College',
                'college_id': 'DEMO001',
                'designation': 'Principal'
            }
        )
        print("✅ Admin user created")
    
    # Create demo alumni
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
        },
        {
            'username': 'mike.johnson',
            'email': 'mike.johnson@email.com',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'branch': 'ME',
            'batch_year': 2017,
            'cgpa': 8.8,
            'current_company': 'Tesla',
            'current_position': 'Senior Engineer',
            'work_experience': 6,
            'is_mentor': False
        }
    ]
    
    for data in alumni_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            
            profile, _ = Profile.objects.get_or_create(
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
    
    # Create demo students
    student_data = [
        {
            'username': 'alice.wilson',
            'email': 'alice.wilson@student.edu',
            'first_name': 'Alice',
            'last_name': 'Wilson',
            'branch': 'CSE',
            'batch_year': 2022,
            'current_semester': 6,
            'cgpa': 8.2,
            'college_name': 'Demo Engineering College'
        },
        {
            'username': 'bob.brown',
            'email': 'bob.brown@student.edu',
            'first_name': 'Bob',
            'last_name': 'Brown',
            'branch': 'ECE',
            'batch_year': 2023,
            'current_semester': 4,
            'cgpa': 7.8,
            'college_name': 'Demo Engineering College'
        }
    ]
    
    for data in student_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            
            profile, _ = Profile.objects.get_or_create(
                user=user,
                defaults={'user_type': 'student'}
            )
            
            Student.objects.get_or_create(
                profile=profile,
                defaults={
                    'batch_year': data['batch_year'],
                    'branch': data['branch'],
                    'current_semester': data['current_semester'],
                    'cgpa': data['cgpa'],
                    'college_name': data['college_name']
                }
            )
            print(f"✅ Student {data['first_name']} {data['last_name']} created")

def create_demo_events():
    """Create demo events"""
    print("Creating demo events...")
    
    try:
        admin = CollegeAdmin.objects.first()
        if not admin:
            print("❌ No admin found. Please create an admin user first.")
            return
        
        events_data = [
            {
                'title': 'Alumni Meet 2024',
                'description': 'Annual alumni gathering to celebrate achievements and network with fellow graduates.',
                'event_date': timezone.now() + timedelta(days=30),
                'venue': 'Main Auditorium',
                'registration_fee': 500,
                'max_participants': 100
            },
            {
                'title': 'Tech Talk Series',
                'description': 'Industry experts sharing insights on latest technology trends.',
                'event_date': timezone.now() + timedelta(days=45),
                'venue': 'Conference Room',
                'registration_fee': 0,
                'max_participants': 50
            },
            {
                'title': 'Career Fair',
                'description': 'Connect with recruiters and explore job opportunities.',
                'event_date': timezone.now() + timedelta(days=60),
                'venue': 'Sports Complex',
                'registration_fee': 200,
                'max_participants': 200
            }
        ]
        
        for data in events_data:
            Event.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'event_date': data['event_date'],
                    'venue': data['venue'],
                    'registration_fee': data['registration_fee'],
                    'max_participants': data['max_participants'],
                    'created_by': admin
                }
            )
            print(f"✅ Event '{data['title']}' created")
    
    except Exception as e:
        print(f"❌ Error creating events: {e}")

def create_demo_internships():
    """Create demo internships"""
    print("Creating demo internships...")
    
    alumni = Alumni.objects.filter(is_mentor=True).first()
    if not alumni:
        print("❌ No alumni found. Please create alumni users first.")
        return
    
    internships_data = [
        {
            'company_name': 'Tech Solutions Pvt Ltd',
            'position': 'Software Development Intern',
            'description': 'We are looking for a motivated software development intern to join our team.',
            'requirements': 'Knowledge of programming languages (Python, Java, or C++), Understanding of software development lifecycle',
            'duration_months': 6,
            'stipend': 15000,
            'location': 'Bangalore, Karnataka',
            'contact_email': 'hr@techsolutions.com'
        },
        {
            'company_name': 'Innovation Labs',
            'position': 'Data Science Intern',
            'description': 'Exciting opportunity to work on real-world data science projects.',
            'requirements': 'Python, Machine Learning, Statistics, Data Analysis',
            'duration_months': 8,
            'stipend': 12000,
            'location': 'Mumbai, Maharashtra',
            'contact_email': 'careers@innovationlabs.com'
        }
    ]
    
    for data in internships_data:
        Internship.objects.get_or_create(
            company_name=data['company_name'],
            position=data['position'],
            defaults={
                'description': data['description'],
                'requirements': data['requirements'],
                'duration_months': data['duration_months'],
                'stipend': data['stipend'],
                'location': data['location'],
                'contact_email': data['contact_email'],
                'posted_by': alumni
            }
        )
        print(f"✅ Internship '{data['position']}' at {data['company_name']} created")

def main():
    """Main function to create all demo data"""
    print("🚀 Creating demo data for Alumni Connect Platform...")
    
    try:
        create_demo_users()
        create_demo_events()
        create_demo_internships()
        
        print("\n🎉 Demo data creation completed successfully!")
        print("\n📋 Demo Accounts Created:")
        print("👨‍💼 Admin: username='admin', password='admin123'")
        print("👨‍🎓 Alumni: username='john.doe', password='password123'")
        print("👩‍🎓 Alumni: username='jane.smith', password='password123'")
        print("👨‍🎓 Alumni: username='mike.johnson', password='password123'")
        print("👩‍🎓 Student: username='alice.wilson', password='password123'")
        print("👨‍🎓 Student: username='bob.brown', password='password123'")
        
        print("\n🌐 You can now:")
        print("1. Run the server: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/")
        print("3. Login with any of the demo accounts above")
        
    except Exception as e:
        print(f"❌ Error creating demo data: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
Script to create admin user without interactive password input
This solves the createsuperuser password input issue
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_platform.settings')
django.setup()

from django.contrib.auth.models import User
from main_app.models import Profile, CollegeAdmin

def create_admin_user():
    """Create admin user with predefined credentials"""
    print("🔧 Creating admin user...")
    
    # Default admin credentials
    username = 'admin'
    email = 'admin@college.edu'
    password = 'admin123'
    first_name = 'College'
    last_name = 'Administrator'
    
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
            first_name=first_name,
            last_name=last_name,
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
        print(f"   Email: {email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

def create_custom_admin():
    """Create admin user with custom credentials"""
    print("\n🔧 Creating custom admin user...")
    
    # Get input from user
    username = input("Enter admin username (default: admin): ").strip() or 'admin'
    email = input("Enter admin email (default: admin@college.edu): ").strip() or 'admin@college.edu'
    password = input("Enter admin password (default: admin123): ").strip() or 'admin123'
    first_name = input("Enter first name (default: College): ").strip() or 'College'
    last_name = input("Enter last name (default: Administrator): ").strip() or 'Administrator'
    college_name = input("Enter college name (default: Demo Engineering College): ").strip() or 'Demo Engineering College'
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"⚠️  User '{username}' already exists")
        choice = input("Do you want to update the password? (y/n): ").strip().lower()
        if choice == 'y':
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print("✅ Password updated successfully!")
            return True
        else:
            return False
    
    try:
        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
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
                'college_name': college_name,
                'college_id': f'ADMIN{user.id:03d}',
                'designation': 'Administrator'
            }
        )
        
        print("✅ Custom admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Email: {email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating custom admin user: {e}")
        return False

def list_admin_users():
    """List all admin users"""
    print("\n👥 Current admin users:")
    admin_users = User.objects.filter(is_superuser=True)
    
    if not admin_users.exists():
        print("   No admin users found")
        return
    
    for user in admin_users:
        try:
            college_admin = CollegeAdmin.objects.get(profile__user=user)
            college_info = f" ({college_admin.college_name})"
        except:
            college_info = ""
        
        print(f"   • {user.username} - {user.email}{college_info}")

def reset_admin_password():
    """Reset admin password"""
    print("\n🔑 Reset admin password...")
    
    username = input("Enter username to reset password: ").strip()
    
    try:
        user = User.objects.get(username=username)
        if not user.is_superuser:
            print("❌ User is not an admin")
            return False
        
        password = input("Enter new password: ").strip()
        if not password:
            print("❌ Password cannot be empty")
            return False
        
        user.set_password(password)
        user.save()
        
        print(f"✅ Password reset successfully for user '{username}'")
        return True
        
    except User.DoesNotExist:
        print(f"❌ User '{username}' not found")
        return False
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        return False

def main():
    """Main function"""
    print("Alumni Connect Platform - Admin User Manager")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Create default admin user (username: admin, password: admin123)")
        print("2. Create custom admin user")
        print("3. List all admin users")
        print("4. Reset admin password")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            create_admin_user()
        elif choice == '2':
            create_custom_admin()
        elif choice == '3':
            list_admin_users()
        elif choice == '4':
            reset_admin_password()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

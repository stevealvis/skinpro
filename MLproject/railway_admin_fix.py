#!/usr/bin/env python
"""
Railway Deployment Admin Fix Script
This script helps fix admin login issues on Railway deployment
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disease_prediction.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command

def check_admin_status():
    """Check if admin user exists and display status"""
    print("=" * 60)
    print("ADMIN STATUS CHECK")
    print("=" * 60)
    
    # Check if admin user exists
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✓ Admin user found:")
        print(f"  - Username: {admin_user.username}")
        print(f"  - Email: {admin_user.email}")
        print(f"  - Is Superuser: {admin_user.is_superuser}")
        print(f"  - Is Staff: {admin_user.is_staff}")
        print(f"  - Is Active: {admin_user.is_active}")
        
        # Check password
        if admin_user.check_password('admin123'):
            print(f"  - Password: admin123 (default)")
        else:
            print(f"  - Password: [CHANGED]")
            
    except User.DoesNotExist:
        print("✗ Admin user does not exist!")
        return False
    except Exception as e:
        print(f"✗ Error checking admin user: {e}")
        return False
    
    # Check all users
    total_users = User.objects.count()
    superusers = User.objects.filter(is_superuser=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    print(f"\nDatabase Statistics:")
    print(f"  - Total users: {total_users}")
    print(f"  - Superusers: {superusers}")
    print(f"  - Staff users: {staff_users}")
    
    return True

def create_admin_user():
    """Create admin user if it doesn't exist"""
    print("\n" + "=" * 60)
    print("CREATING ADMIN USER")
    print("=" * 60)
    
    try:
        # Use Django management command
        call_command('create_admin_user', '--force')
        print("\n✓ Admin user created/updated successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Error creating admin user: {e}")
        
        # Fallback: Manual creation
        try:
            if not User.objects.filter(username='admin').exists():
                admin_user = User.objects.create_superuser(
                    username='admin',
                    email='admin@admin.com',
                    password='admin123'
                )
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.save()
                print("✓ Admin user created manually!")
                return True
            else:
                print("Admin user already exists (manual check)")
                return True
        except Exception as e2:
            print(f"✗ Manual creation also failed: {e2}")
            return False

def run_migrations():
    """Run Django migrations"""
    print("\n" + "=" * 60)
    print("RUNNING MIGRATIONS")
    print("=" * 60)
    
    try:
        call_command('migrate', '--run-syncdb')
        print("✓ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Migration error: {e}")
        return False

def main():
    """Main function to fix admin issues"""
    print("RAILWAY ADMIN LOGIN FIX")
    print("This script will help fix admin login issues on Railway deployment")
    
    # Step 1: Check current status
    admin_exists = check_admin_status()
    
    # Step 2: Run migrations if needed
    run_migrations()
    
    # Step 3: Create admin user if needed
    if not admin_exists:
        create_admin_user()
    else:
        print("\n" + "=" * 60)
        print("ADMIN USER ALREADY EXISTS")
        print("=" * 60)
        print("If you're still having login issues:")
        print("1. Try logging in with:")
        print("   Username: admin")
        print("   Password: admin123")
        print("2. If that doesn't work, run with --force flag")
        print("3. Check if the deployed site is using the correct database")
    
    # Final check
    print("\n" + "=" * 60)
    print("FINAL STATUS CHECK")
    print("=" * 60)
    check_admin_status()
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Deploy your changes to Railway")
    print("2. Run this script on Railway: python railway_admin_fix.py")
    print("3. Try logging in at: https://your-app.railway.app/accounts/sign_in_admin")
    print("4. If issues persist, check Railway logs for errors")

if __name__ == '__main__':
    main()

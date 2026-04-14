#!/usr/bin/env python
"""
Django management command to create admin user in production
Usage: python manage.py create_admin_user
"""
import os
import django
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates an admin superuser with default credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Admin username (default: admin)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@admin.com',
            help='Admin email (default: admin@admin.com)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Admin password (default: admin123)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreate if admin already exists'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        force = options['force']

        # Check if admin already exists
        try:
            admin_user = User.objects.get(username=username)
            if force:
                self.stdout.write(
                    self.style.WARNING(f'Admin user "{username}" already exists. Deleting and recreating...')
                )
                admin_user.delete()
                # Delete any existing patient/doctor profiles
                from main_app.models import patient, doctor
                patient.objects.filter(user=admin_user).delete()
                doctor.objects.filter(user=admin_user).delete()
            else:
                self.stdout.write(
                    self.style.ERROR(f'Admin user "{username}" already exists. Use --force to recreate.')
                )
                return
        except User.DoesNotExist:
            pass

        # Create new admin user
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'Admin user "{username}" created successfully!')
            )
            self.stdout.write(f'Username: {username}')
            self.stdout.write(f'Email: {email}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write(
                self.style.WARNING('Please change the default password after first login!')
            )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )

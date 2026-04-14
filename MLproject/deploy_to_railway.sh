#!/bin/bash
# Railway Deployment Script for Admin Fix
# This script should be run after deploying to Railway

echo "🚀 Railway Admin Login Fix Deployment Script"
echo "=============================================="

# Navigate to the app directory
cd /app 2>/dev/null || cd /Users/ankuankit/Desktop/pro/Skin

echo "📋 Step 1: Running Django migrations..."
python manage.py migrate --run-syncdb

echo "📋 Step 2: Creating admin user..."
python manage.py create_admin_user --force

echo "📋 Step 3: Running diagnostic check..."
python railway_admin_fix.py

echo "✅ Deployment completed!"
echo ""
echo "🔐 Admin Login Credentials:"
echo "   URL: https://your-app.railway.app/accounts/sign_in_admin"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🔧 Django Admin (alternative):"
echo "   URL: https://your-app.railway.app/admin/"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change the default password after first login!"
echo ""
echo "📖 For detailed instructions, see ADMIN_FIX_README.md"

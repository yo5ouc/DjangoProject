import os
import sys
import django

# Tell Python to look in the current root folder for modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 🔐 Pull the credentials safely from Render's Environment
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'local-admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'local-password')
email = 'yo5ouc@gmail.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("🚀 Superuser created successfully from environment variables!")
else:
    print("✅ Superuser already exists. Skipping creation to protect your data.")

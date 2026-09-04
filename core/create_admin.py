import os
import sys
import django

# Tell Python to look in the current root folder for modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Station

User = get_user_model()

# 🔐 1. Superuser Setup (YO5OUC)
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'local-admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'local-password')
email = 'yo5ouc@gmail.com'

admin_user, created = User.objects.get_or_create(
    username=username,
    defaults={'email': email, 'is_staff': True, 'is_superuser': True}
)
if not created:
    admin_user.is_staff = True
    admin_user.is_superuser = True
admin_user.set_password(password)
admin_user.save()

if created:
    print("🚀 Superuser created successfully from environment variables!")
else:
    print("✅ Superuser updated/verified successfully.")

# Automatically provision station for superuser
station1, _ = Station.objects.get_or_create(
    callsign="YO5OUC",
    defaults={'owner': admin_user, 'is_active': True}
)
print(f"📡 Station {station1.callsign} assigned to {username}.")


# 🔐 2. Regular Operator Setup (YO5YM)
regular_username = os.environ.get('REGULAR_USER_NAME', 'local-operator')
regular_password = os.environ.get('REGULAR_USER_PASSWORD', 'local-user-password')
regular_email = 'yo5ouc@gmail.com'

op_user, created = User.objects.get_or_create(
    username=regular_username,
    defaults={'email': regular_email, 'is_staff': True}
)
if not created:
    op_user.is_staff = True
op_user.set_password(regular_password)
op_user.save()

if created:
    print("👤 Regular user created successfully from environment variables!")
else:
    print("✅ Regular user updated/verified successfully.")

# Automatically provision station for regular operator
station2, _ = Station.objects.get_or_create(
    callsign="YO5YM",
    defaults={'owner': op_user, 'is_active': True}
)
print(f"📡 Station {station2.callsign} assigned to {regular_username}.")
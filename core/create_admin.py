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

# Change these to the username and password you want!
username = 'admin'
password = 'dfrt54DFG342**&;.,hgfrte'
email = 'yo5ouc@gmail.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")

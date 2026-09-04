import secrets
from django.db import models
from django.contrib.auth.models import User

def generate_bridge_key():
    return secrets.token_urlsafe(32)

class Station(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="station")
    callsign = models.CharField(max_length=15, unique=True, help_text="e.g. YO5OUC")
    bridge_secret_key = models.CharField(max_length=64, default=generate_bridge_key, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.callsign} ({self.owner.username})"
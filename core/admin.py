from django.contrib import admin
from .models import Station

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("callsign", "owner", "bridge_secret_key", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("callsign", "owner__username", "bridge_secret_key")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Station Identity", {
            "fields": ("callsign", "owner", "is_active")
        }),
        ("Security & Bridge Credentials", {
            "fields": ("bridge_secret_key",),
            "description": "Copy this token into the STATION_KEY setting inside the operator's rig_bridge.py script."
        }),
        ("Timestamps", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )
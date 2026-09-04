from django.urls import re_path
from core import consumers

websocket_urlpatterns = [
    re_path(r'^ws/radio/(?P<callsign>\w+)/?$', consumers.RadioConsumer.as_asgi()),
    # Keep the fallback pattern below if you have any legacy tools connecting without a callsign
    re_path(r'^ws/radio/?$', consumers.RadioConsumer.as_asgi()),
]
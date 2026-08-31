from django.urls import re_path
from core import consumers

websocket_urlpatterns = [
    re_path(r'^ws/radio/$', consumers.RadioConsumer.as_asgi()),
]
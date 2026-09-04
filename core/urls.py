"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from core import views

urlpatterns = [
# General station directory
    path("radio/", views.station_directory, name="station_directory"),
    # Dedicated station console: e.g. /radio/yo5ouc/ or /radio/yo5xyz/
    path("radio/<slug:station_id>/", views.radio_console, name="radio_console"),
# Automatically redirect "/" to "/radio/"
    path('', RedirectView.as_view(url='/radio/', permanent=False)),
    path('admin/', admin.site.urls),
# 📻 Your new transceiver console and api endpoints
    path('radio/', views.radio_dashboard, name='radio_dashboard'),
    path('api/select-band/', views.select_band_api, name='select_band'),
    path('api/select-shift/', views.select_shift_api, name='select_shift'),
    path('api/update-rig/', views.update_telemetry_api, name='update_telemetry'),
    path('api/get-status/', views.get_status_api, name='get_status'),
]

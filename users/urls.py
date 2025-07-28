"""Defines URL patterns for the users app."""

from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # Include default auth urls.
    # This line includes predefined URLs for login, logout, password management, etc.
    path('', include('django.contrib.auth.urls')),

    # Registration page
    path('register/', views.register, name='register'),
]
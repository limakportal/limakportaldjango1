from django.contrib import admin
from django.urls import path

from .views import GoogleView 

urlpatterns = [
    path('logintest', GoogleView.as_view(),name="logintest"),
]
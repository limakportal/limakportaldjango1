from django.contrib import admin
from django.urls import path

from .views import GoogleView 

urlpatterns = [
    path('googleLogin', GoogleView.as_view(),name="googleLogin"),
]
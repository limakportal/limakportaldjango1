from django.urls import path
from .views import VocationAPIView


urlpatterns = [ 
    path('vocationdays',VocationAPIView.as_view())
]
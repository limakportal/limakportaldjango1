from django.urls import path
from .views import PermissionAPIView , PermissionDetails


urlpatterns = [ 
    path('permissions', PermissionAPIView.as_view()),
    path('permissions/<int:id>/', PermissionDetails.as_view()),
]
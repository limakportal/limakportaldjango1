from django.urls import path
from .views import RoleAPIView , RoleDetails


urlpatterns = [ 
    path('roles', RoleAPIView.as_view()),
    path('roles/<int:id>/', RoleDetails.as_view()),
]
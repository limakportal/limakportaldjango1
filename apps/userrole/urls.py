from django.urls import path
from .views import UserRoleAPIView , UserRoleDetails

urlpatterns = [ 
    path('userroles', UserRoleAPIView.as_view()),
    path('userroles/<int:id>/', UserRoleDetails.as_view()),
]
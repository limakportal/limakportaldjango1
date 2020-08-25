from django.urls import path
from .views import RoleAPIView , RoleDetails
from .businesrules import RoleWithPermissionAPIView , RoleWithPermissionDetails


urlpatterns = [ 
    path('roles', RoleAPIView.as_view()),
    path('roles/<int:id>', RoleDetails.as_view()),
    path('rolewithpermission', RoleWithPermissionAPIView.as_view()),
    path('rolewithpermission/<int:id>', RoleWithPermissionDetails.as_view()),
]
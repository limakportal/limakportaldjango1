from django.urls import path
from .views import OrganizationAPIView , OrganizationDetails , OrganizationTreeList


urlpatterns = [ 
    path('organizations', OrganizationAPIView.as_view()),
    path('organizations/<int:id>/', OrganizationDetails.as_view()),
    path('organizationTree', OrganizationTreeList.as_view()),
]
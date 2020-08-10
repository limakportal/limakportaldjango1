from django.urls import path
from .views import OrganizationAPIView , OrganizationDetails


urlpatterns = [ 
    path('organizations/', OrganizationAPIView.as_view()),
    path('organization/<int:id>/', OrganizationDetails.as_view()),
]
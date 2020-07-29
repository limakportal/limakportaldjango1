from django.urls import path
from .views import OrganizationTypeAPIView , OrganizationTypeDetails


urlpatterns = [ 
    path('organizationtypes/', OrganizationTypeAPIView.as_view()),
    path('organizationtype/', OrganizationTypeDetails.as_view()),
]
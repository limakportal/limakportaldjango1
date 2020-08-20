from django.urls import path
from .views import OrganizationTypeAPIView , OrganizationTypeDetails


urlpatterns = [ 
    path('organizationTypes', OrganizationTypeAPIView.as_view()),
    path('organizationTypes/<int:id>', OrganizationTypeDetails.as_view()),
]
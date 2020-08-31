from django.urls import path
from .views import AnnouncmentOrganizationAPIView , AnnouncmentOrganizationDetails


urlpatterns = [ 
    path('announcmentorganizations', AnnouncmentOrganizationAPIView.as_view()),
    path('announcmentorganizations/<int:id>', AnnouncmentOrganizationDetails.as_view()),
]
from django.urls import path
from .views import AnnouncmentAPIView , AnnouncmentDetails


urlpatterns = [ 
    path('announcment', AnnouncmentAPIView.as_view()),
    path('announcment/<int:id>', AnnouncmentDetails.as_view()),
]
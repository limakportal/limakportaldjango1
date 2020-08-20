from django.urls import path
from .views import NationalityAPIView , NationalityDetails


urlpatterns = [ 
    path('nationalities', NationalityAPIView.as_view()),
    path('nationalities/<int:id>', NationalityDetails.as_view()),
]
from django.urls import path
from .views import CityAPIView , CityDetails


urlpatterns = [ 
    path('cities', CityAPIView.as_view()),
    path('cities/<int:id>/', CityDetails.as_view()),
]
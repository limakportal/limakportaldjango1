from django.urls import path
from .views import DistrictAPIView , DistrictDetails


urlpatterns = [ 
    path('district', DistrictAPIView.as_view()),
    path('district/<int:id>/', DistrictDetails.as_view()),
]
from django.urls import path
from .views import DistrictAPIView , DistrictDetails


urlpatterns = [ 
    path('districts/', DistrictAPIView.as_view()),
    path('district/', DistrictDetails.as_view()),
]
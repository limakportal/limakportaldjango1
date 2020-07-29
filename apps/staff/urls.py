from django.urls import path
from .views import StaffAPIView , StaffDetails


urlpatterns = [ 
    path('staffs/', StaffAPIView.as_view()),
    path('staff/', StaffDetails.as_view()),
]
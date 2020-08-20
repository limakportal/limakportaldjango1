from django.urls import path
from .views import StaffAPIView , StaffDetails


urlpatterns = [ 
    path('staff', StaffAPIView.as_view()),
    path('staff/<int:id>', StaffDetails.as_view()),
]
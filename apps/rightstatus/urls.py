from django.urls import path
from .views import RightStatusAPIView , RightStatusDetails


urlpatterns = [ 
    path('rightstatuses/', RightStatusAPIView.as_view()),
    path('rightstatus/<int:id>/', RightStatusDetails.as_view()),
]
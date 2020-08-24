from django.urls import path
from .views import ShiftAPIView , ShiftDetails

urlpatterns = [ 
    path('shifts', ShiftAPIView.as_view()),
    path('shifts/<int:id>/', ShiftDetails.as_view()),
]
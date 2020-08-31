from django.urls import path
from .views import VocationAPIView , VocationDetails, VocationDaysByMonthh


urlpatterns = [ 
    path('vocationdays',VocationAPIView.as_view()),
    path('vocationdays/<int:id>', VocationDetails.as_view()),
    path('vocationdaysbymonth/<int:month>', VocationDaysByMonthh),
]
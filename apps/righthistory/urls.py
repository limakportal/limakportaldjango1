from django.urls import path
from .views import RightHistoryAPIView , RightHistoryDetails


urlpatterns = [ 
    path('rightHistoryes', RightHistoryAPIView.as_view()),
    path('rightHistoryes/<int:id>/', RightHistoryDetails.as_view()),
]
from django.urls import path
from .views import RightHistoryAPIView , RightHistoryDetails


urlpatterns = [ 
    path('righthistories/', RightHistoryAPIView.as_view()),
    path('righthistory/<int:id>/', RightHistoryDetails.as_view()),
]
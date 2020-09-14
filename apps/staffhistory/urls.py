from django.urls import path
from .views import StaffHistoryAPIView, StaffHistoryDetails

urlpatterns = [
    path('staffhistory', StaffHistoryAPIView.as_view()),
    path('staffhistory/<int:id>/', StaffHistoryDetails.as_view()),
]

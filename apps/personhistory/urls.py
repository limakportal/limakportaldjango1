from django.urls import path
from .views import PersonHistoryAPIView , PersonHistoryDetails


urlpatterns = [ 
    path('personhistories/', PersonHistoryAPIView.as_view()),
    path('personhistory/<int:id>/', PersonHistoryDetails.as_view()),
]
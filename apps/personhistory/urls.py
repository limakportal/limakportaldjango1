from django.urls import path
from .views import PersonHistoryAPIView , PersonHistoryDetails


urlpatterns = [ 
    path('personhistories/', PersonHistoryAPIView.as_view()),
    path('personhistories/<int:id>/', PersonHistoryDetails.as_view()),
]
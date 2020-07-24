from django.urls import path
from .views import PersonAPIView , PersonDetails


urlpatterns = [ 
    path('person/', PersonAPIView.as_view()),
    path('person/detail/<int:id>/', PersonDetails.as_view()),
]
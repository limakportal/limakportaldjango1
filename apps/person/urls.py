from django.urls import path
from .views import PersonAPIView , PersonDetails 


urlpatterns = [ 
    path('persons/', PersonAPIView.as_view()),
    path('persons/<int:id>/', PersonDetails.as_view()),
]
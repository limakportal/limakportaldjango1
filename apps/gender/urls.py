from django.urls import path
from .views import GenderAPIView 


urlpatterns = [ 
    path('gender/', GenderAPIView.as_view()),
    # path('gender/detail/<int:id>/', PersonDetails.as_view()),
]
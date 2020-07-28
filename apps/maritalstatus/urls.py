from django.urls import path
from .views import MaritalStatusAPIView 


urlpatterns = [ 
    path('maritalstatuses/', MaritalStatusAPIView.as_view()),
    # path('gender/detail/<int:id>/', PersonDetails.as_view()),
]
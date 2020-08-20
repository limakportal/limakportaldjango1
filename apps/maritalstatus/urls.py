from django.urls import path
from .views import MaritalStatusAPIView , MaritalStatusDetails


urlpatterns = [ 
    path('maritalstatuses', MaritalStatusAPIView.as_view()),
    path('maritalstatuses/<int:id>', MaritalStatusDetails.as_view()),
]
from django.urls import path
from .views import NationalityAPIView


urlpatterns = [ 
    path('nationalities/', NationalityAPIView.as_view()),
    # path('gender/detail/<int:id>/', PersonDetails.as_view()),
]
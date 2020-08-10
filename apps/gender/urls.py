from django.urls import path
from .views import GenderAPIView , GenderDetails


urlpatterns = [ 
    path('genders/', GenderAPIView.as_view()),
    path('genders/<int:id>/', GenderDetails.as_view()),
]
from django.urls import path
from .views import VocationAPIView , VocationDetails


urlpatterns = [ 
    path('vocationdays',VocationAPIView.as_view()),
    path('vocationdays/<int:id>', VocationDetails.as_view()),
]
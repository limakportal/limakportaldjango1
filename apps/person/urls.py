from django.urls import path
from .views import PersonelAPIView , PersonelDetails


urlpatterns = [ 
    path('personel/', PersonelAPIView.as_view()),
    path('personel/detail/<int:id>/', PersonelDetails.as_view()),
]
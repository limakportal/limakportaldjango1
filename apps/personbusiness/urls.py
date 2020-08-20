from django.urls import path
from .views import PersonBusinessAPIView , PersonBusinessDetails


urlpatterns = [ 
    path('personbusinesses', PersonBusinessAPIView.as_view()),
    path('personbusinesses/<int:id>/', PersonBusinessDetails.as_view()),
]
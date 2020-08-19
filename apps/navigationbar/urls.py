from django.urls import path
from .views import NavigationBarAPIView , NavigationBarDetails


urlpatterns = [ 
    path('navigationbar/', NavigationBarAPIView.as_view()),
    path('navigationbar/<int:id>/', NavigationBarDetails.as_view()),
]
from django.urls import path
from .views import NavigationBarAPIView , NavigationBarDetails


urlpatterns = [ 
    path('navigationbars', NavigationBarAPIView.as_view()),
    path('navigationbars/<int:id>', NavigationBarDetails.as_view()),
]
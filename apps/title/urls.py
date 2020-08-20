from django.urls import path
from .views import TitleAPIView , TitleDetails


urlpatterns = [ 
    path('titles', TitleAPIView.as_view()),
    path('titles/<int:id>', TitleDetails.as_view()),
]
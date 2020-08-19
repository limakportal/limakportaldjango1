from django.urls import path
from .views import AuthorityAPIView , AuthorityDetails


urlpatterns = [ 
    path('authorities/', AuthorityAPIView.as_view()),
    path('authorities/<int:id>/', AuthorityDetails.as_view()),
]
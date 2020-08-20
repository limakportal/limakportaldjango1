from django.urls import path
from .views import PersonIdentityAPIView , PersonIdentityDetails


urlpatterns = [ 
    path('personIdentitys', PersonIdentityAPIView.as_view()),
    path('personIdentitys/<int:id>/', PersonIdentityDetails.as_view()),
]
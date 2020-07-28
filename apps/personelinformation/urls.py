from django.urls import path
from .views import PersonelInformationAPIView , PersonelInformationDetails


urlpatterns = [ 
    path('personelinformations/', PersonelInformationAPIView.as_view()),
    path('personelinformation/<int:id>/', PersonelInformationDetails.as_view()),
]
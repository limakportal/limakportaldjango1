from django.urls import path
from apps.personelinformation.views import PersonelInformationAPIView , PersonelInformationDetails


urlpatterns = [ 
    path('personalinformations/', PersonelInformationAPIView.as_view()),
    path('personalinformations/<int:id>/', PersonelInformationDetails.as_view()),
]
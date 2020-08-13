from django.urls import path
from .views import PersonFamilyAPIView , PersonFamilyDetails


urlpatterns = [ 
    path('personfamilys/', PersonFamilyAPIView.as_view()),
    path('personfamilys/<int:id>/', PersonFamilyDetails.as_view()),
]
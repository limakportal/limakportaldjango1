from django.urls import path
from .views import PersonEmploymentAPIView , PersonEmploymentDetails


urlpatterns = [ 
    path('personemployment', PersonEmploymentAPIView.as_view()),
    path('personemployment/<int:id>', PersonEmploymentDetails.as_view()),
]
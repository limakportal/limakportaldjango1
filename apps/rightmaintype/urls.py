from django.urls import path
from .views import RightMainTypeAPIView , RightMainTypeDetails


urlpatterns = [ 
    path('rightmaintypes/', RightMainTypeAPIView.as_view()),
    path('rightmaintypes/<int:id>/', RightMainTypeDetails.as_view()),
]
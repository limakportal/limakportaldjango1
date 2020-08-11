from django.urls import path
from .views import RightAPIView , RightDetails


urlpatterns = [ 
    path('rights/', RightAPIView.as_view()),
    path('rights/<int:id>/', RightDetails.as_view()),
]
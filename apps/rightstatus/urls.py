from django.urls import path
from .views import RightStatusAPIView , RightStatusDetails


urlpatterns = [ 
    path('rightStatuses', RightStatusAPIView.as_view()),
    path('rightStatuses/<int:id>', RightStatusDetails.as_view()),
]
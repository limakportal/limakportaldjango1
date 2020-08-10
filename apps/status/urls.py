from django.urls import path
from .views import StatusAPIView ,StatusDetails


urlpatterns = [ 
    path('statuses/', StatusAPIView.as_view()),
    path('statuses/<int:id>/', StatusDetails.as_view()),
]
from django.urls import path
from .views import StatusAPIView 


urlpatterns = [ 
    path('status/', StatusAPIView.as_view()),
    # path('righttype/<int:id>/', StatusDetails.as_view()),
]
from django.urls import path
from .views import RightTypeAPIView , RightTypeDetails


urlpatterns = [ 
    path('righttypes/', RightTypeAPIView.as_view()),
    path('righttype/<int:id>/', RightTypeDetails.as_view()),
]
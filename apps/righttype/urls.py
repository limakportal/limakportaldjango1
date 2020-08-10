from django.urls import path
from .views import RightTypeAPIView , RightTypeDetails


urlpatterns = [ 
    path('rightTypes/', RightTypeAPIView.as_view()),
    path('rightTypes/<int:id>/', RightTypeDetails.as_view()),
]
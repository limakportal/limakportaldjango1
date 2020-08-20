from django.urls import path
from .views import PersonEducationAPIView , PersonEducationDetails


urlpatterns = [ 
    path('personeducations', PersonEducationAPIView.as_view()),
    path('personeducations/<int:id>', PersonEducationDetails.as_view()),
]
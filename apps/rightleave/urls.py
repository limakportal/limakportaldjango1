from django.urls import path
from .views import RightLeaveAPIView , RightLeaveDetails


urlpatterns = [ 
    path('rightleaves/', RightLeaveAPIView.as_view()),
    path('rightleaves/<int:id>', RightLeaveDetails.as_view()),
]
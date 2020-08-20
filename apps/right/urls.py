from django.urls import path
from .views import RightAPIView , RightDetails , RightWithApproverAPIView,RightDownload


urlpatterns = [ 
    path('rights', RightAPIView.as_view()),
    path('rights/<int:id>/', RightDetails.as_view()),
    path('rightsDesc', RightWithApproverAPIView.as_view()),
    path('rightsDownload', RightDownload)
]
from django.urls import path
from .views import RightAPIView , RightDetails , RightWithApproverAPIView, RightDownloadApiView, RightBalance, RightDaysNumber ,PersonRightInfo


urlpatterns = [ 
    path('rights', RightAPIView.as_view()),
    path('rights/<int:id>', RightDetails.as_view()),
    path('rightsDesc', RightWithApproverAPIView.as_view()),
    path('rightsDownload/<int:id>', RightDownloadApiView.as_view()),
    path('rightsBalance/<int:id>', RightBalance),
    path('righsDayNumber', RightDaysNumber),
    path('personRightInfo/<int:id>', PersonRightInfo)
]
from django.urls import path
from .views import( 
    RightAPIView , 
    RightDetails , 
    RightWithApproverAPIView, 
    RightDownloadApiView, 
    RightBalance, 
    RightDaysNumber ,
    PersonRightInfo, 
    GetRightStatus, 
    TodayOnLeavePerson, 
    RightAllDetails,
    RightSummary,
    RightWithApproverDetail  
)



urlpatterns = [ 
    path('rights', RightAPIView.as_view()),
    path('rights/<int:id>', RightDetails.as_view()),
    path('rightsDesc', RightWithApproverAPIView.as_view()),
    path('rightsDesc/<int:id>', RightWithApproverDetail.as_view()),
    path('rightsDownload/<int:id>', RightDownloadApiView.as_view()),
    path('rightsBalance/<int:id>', RightBalance),
    path('righsDayNumber', RightDaysNumber),
    path('personRightInfo/<int:id>', PersonRightInfo),
    path('getrightstatus/<int:status_id>', GetRightStatus),
    path('todayonleaveperson', TodayOnLeavePerson),
    path('rightalldetails', RightAllDetails),
    path('rightsummary/<int:id>', RightSummary),
  
]
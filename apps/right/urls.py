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
    RightWithApproverDetail,
    ApproveRight,
    DenyRight,
    CancelRight,
    TodayOnLeavePersonByPerson,
    PersonRightInfoPerson,
    HasField
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
    path('personRightInfoByPerson/<int:id>', PersonRightInfoPerson),
    path('getrightstatus/<int:status_id>', GetRightStatus),
    path('todayonleaveperson', TodayOnLeavePerson),
    path('todayonleaveperson/<int:id>', TodayOnLeavePersonByPerson),
    path('rightalldetails', RightAllDetails),
    path('rightsummary/<int:id>', RightSummary),
    path('approveright/<int:id>', ApproveRight),
    path('denyright/<int:id>', DenyRight),
    path('cancelright/<int:id>', CancelRight),
    path('hasfield/<int:id>', HasField),
  
]
from django.urls import path
from .views import StaffAPIView , StaffDetails
from .businesrules import GetResponsibleStaff


urlpatterns = [ 
    path('staff', StaffAPIView.as_view()),
    path('getresponsiblestaff', GetResponsibleStaff),
    path('staff/<int:id>', StaffDetails.as_view()),
]
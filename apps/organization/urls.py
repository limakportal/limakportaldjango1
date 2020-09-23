from django.urls import path
from .views import (OrganizationAPIView,
                    OrganizationDetails,
                    OrganizationTreeList)
from .businesrules import GetResponsibleOrganization

urlpatterns = [
    path('organizations', OrganizationAPIView.as_view()),
    path('organizations/<int:id>', OrganizationDetails.as_view()),
    path('organizationTree', OrganizationTreeList.as_view()),
    path('getresponsibleorganization', GetResponsibleOrganization),
]

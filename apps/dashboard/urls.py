from django.urls import path

from .views import (
    GetResponsiblePersons,
    GetPersonCountWithOrganization,
    GetOrganizationResponsiblePersons,
    GetOrganizationWithTotalStaff,
    GetAllOrganizationtypeId2WithTotalStaff
)

urlpatterns = [
    path('getresponsiblepersons/<int:id>', GetResponsiblePersons),
    path('getorganizationresponsiblepersons/<int:organizationid>', GetOrganizationResponsiblePersons),
    path('getorganizationwithtotalstaff/<int:organizationid>', GetOrganizationWithTotalStaff),
    path('getpersoncountwithorganization', GetPersonCountWithOrganization),
    path('getallorganizationtypeid2withtotalstaff', GetAllOrganizationtypeId2WithTotalStaff),
]

from django.urls import path

from .views import GetResponsiblePersons, GetPersonCountWithOrganization, GetOrganizationResponsiblePersons

urlpatterns = [
    path('getresponsiblepersons/<int:id>', GetResponsiblePersons),
    path('getorganizationresponsiblepersons/<int:organizationid>', GetOrganizationResponsiblePersons),
    path('getpersoncountwithorganization', GetPersonCountWithOrganization),
]

from django.urls import path

from .views import GetResponsiblePersons, GetPersonCountWithOrganization

urlpatterns = [
    path('getresponsiblepersons/<int:id>', GetResponsiblePersons),
    path('getpersoncountwithorganization', GetPersonCountWithOrganization),
]

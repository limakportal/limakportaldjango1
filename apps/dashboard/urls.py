from django.urls import path

from .views import GetResponsiblePersons

urlpatterns = [ 
    path('getresponsiblepersons/<int:id>', GetResponsiblePersons),
]
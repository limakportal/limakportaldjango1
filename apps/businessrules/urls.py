from django.urls import path
from .views import ResponsiblePersonDetails , AccountListDetails, ManagerPersons

urlpatterns = [ 
    path('responsibleperson/<int:id>', ResponsiblePersonDetails),
    path('accountlistdetails', AccountListDetails),
    path('managerpersons',ManagerPersons),
]
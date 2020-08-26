from django.urls import path
from .views import ResponsiblePersonDetails , AccountListDetails

urlpatterns = [ 
    path('responsibleperson/<int:id>', ResponsiblePersonDetails),
    path('accountlistdetails', AccountListDetails),
]
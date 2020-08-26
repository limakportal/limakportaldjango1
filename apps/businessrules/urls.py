from django.urls import path
from .views import ResponsiblePersonDetails

urlpatterns = [ 
    path('responsibleperson/<int:id>', ResponsiblePersonDetails),
]
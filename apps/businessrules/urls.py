from django.urls import path
from .views import PersonList

urlpatterns = [ 
    path('menuwithperson', PersonList.as_view()),
]
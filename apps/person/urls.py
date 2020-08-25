from django.urls import path
from .views import PersonAPIView , PersonDetails , PersonWithPersonInformationAPIView , PersonWithPersonInformationDetails 
from .businesrules import PersonApprover, bornTodayPerson, bornMonthPerson


urlpatterns = [ 
    path('persons', PersonAPIView.as_view()),
    path('persons/<int:id>', PersonDetails.as_view()),
    path('personsDesc', PersonWithPersonInformationAPIView.as_view()),
    path('personsDesc/<int:id>', PersonWithPersonInformationDetails.as_view()),
    path('personapprover/<int:id>', PersonApprover),
    path('borntodayperson', bornTodayPerson),
    path('bornmonthperson', bornMonthPerson),
]
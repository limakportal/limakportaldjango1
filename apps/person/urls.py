from django.urls import path
from .views import PersonWithPersonInformationAPIView , PersonWithPersonInformationDetails , PersonViewSet
from .businesrules import PersonApprover, bornTodayPerson, bornMonthPerson,testSql

from rest_framework import routers


router = routers.DefaultRouter()
router.register('persons', PersonViewSet, basename='persons')


urlpatterns = [
    path('personsDesc', PersonWithPersonInformationAPIView.as_view()),
    path('personsDesc/<int:id>', PersonWithPersonInformationDetails.as_view()),
    path('personapprover/<int:id>', PersonApprover),
    path('borntodayperson', bornTodayPerson),
    path('bornmonthperson', bornMonthPerson),
    path('testSql', testSql),

]

urlpatterns += router.urls

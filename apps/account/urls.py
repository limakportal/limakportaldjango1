from django.urls import path
from apps.account.views import(
    registration_view, ObtainAuthToken
)

app_name = "account"

urlpatterns = [ 
    path('register', registration_view, name="register"),
    path('login', ObtainAuthToken.as_view(), name="login"),
]
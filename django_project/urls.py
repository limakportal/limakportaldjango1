
from django.contrib import admin
from django.urls import path , include

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('',include('apps.person.urls')),
    path('',include('apps.gender.urls')),
    path('',include('apps.right.urls')),
    path('',include('apps.righthistory.urls')),
    path('',include('apps.rightstatus.urls')),
    path('',include('apps.righttype.urls')),
    path('',include('apps.status.urls')),
    path('',include('apps.maritalstatus.urls')),
    path('',include('apps.nationality.urls')),
    path('',include('apps.user.urls')),
    path('',include('apps.district.urls')),
    path('',include('apps.city.urls')),
    path('',include('apps.title.urls')),
    path('',include('apps.organizationtype.urls')),
    path('',include('apps.organization.urls')),
    path('',include('apps.staff.urls')),
    path('',include('apps.account.urls')),
    path('',include('apps.personeducation.urls')),
    path('',include('apps.personidentity.urls')),
    path('',include('apps.personfamily.urls')),
    path('',include('apps.personbusiness.urls')),
    path('',include('apps.navigationbar.urls')),
    path('',include('apps.role.urls')),
    path('',include('apps.permission.urls')),
    path('',include('apps.authority.urls')),
    path('',include('apps.login.urls')),
    path('',include('apps.rightmaintype.urls')),
    path('',include('apps.vocationdays.urls')),
    path('',include('apps.rightleave.urls')),
    path('',include('apps.userrole.urls')),
    path('',include('apps.shift.urls')),
    path('',include('apps.businessrules.urls')),
    path('',include('apps.jwt_token_patched.urls')),
    path('',include('apps.announcment.urls')),
    path('',include('apps.announcmentorganization.urls')),
    path('',include('apps.dashboard.urls')),
]

"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
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
    # path('',include('apps.businessrules.urls')),
]

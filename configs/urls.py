"""configs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import re_path, include
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

api = [
    re_path(r'^applicants/', include('applicants.urls')),
    re_path(r'^values/', include('application_info.urls')),
    re_path(r'^events/', include('events.urls')),
    re_path(r'^rest_auth/', include('rest_auth.urls')),
    re_path(r'^devices/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),

]

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(api))
]

admin.site.site_title = 'TimeTreeAndroid Administration'
admin.site.site_header = 'TimeTreeAndroid Administration'

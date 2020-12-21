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
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

api = [
    path('users/', include('users.urls')),
    path('values/', include('application_info.urls')),
    path('events/', include('events.urls')),
    path('rest_auth/', include('rest_auth.urls')),
    path('devices/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),

]

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/', include(api))
]

admin.site.site_title = _('NeobisTree Administration')
admin.site.site_header = _('NeobisTree Administration')

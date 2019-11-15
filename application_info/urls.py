from django.urls import re_path

from application_info import views

app_name = 'application_info'

urlpatterns = [
    re_path('^$', views.ValuesAPIView.as_view(), name='get_info')
]

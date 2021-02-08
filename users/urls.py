from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path(r'', views.RegistrationAPIView.as_view(), name='registration'),
    path(r'login', views.LoginAPIView.as_view(), name='login'),
    path(r'change_password', views.ChangePasswordAPIView.as_view(), name='change_password'),
    path(r'reset_password', views.ResetPasswordAPIView.as_view(), name='reset_password'),
]

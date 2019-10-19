from django.urls import path

from application_info import views

urlpatterns = [
    path('', views.ValuesAPIView.as_view(), name='values')
]

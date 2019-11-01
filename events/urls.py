from django.urls import path

from events import views

urlpatterns = [
    path(r'', views.EventView.as_view()),
    path(r'book', views.BookView.as_view()),

]

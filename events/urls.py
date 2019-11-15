from django.urls import re_path

from events import views

app_name = 'events'
urlpatterns = [
    re_path(r'^$', views.EventView.as_view(), name='event_list'),
    re_path(r'^book/', views.BookView.as_view(), name='book_room'),
    re_path(r'^set_choice/', views.SetChoiceView.as_view(), name='set_choice'),
    re_path(r'^get_uncertain_users/', views.GetUncertainUsers.as_view(), name='get_uncertain_users')
]

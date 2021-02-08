from django.urls import path

from events import views

app_name = 'events'
urlpatterns = [
    path('', views.EventView.as_view(), name='event_list'),
    path('with_poll/', views.EventWithPollView.as_view(), name='event_list_with_poll'),
    path('book/', views.BookView.as_view(), name='book_room'),
    path('set_choice/', views.SetChoiceView.as_view(), name='set_choice'),
    path('rooms/', views.RoomsView.as_view(), name='rooms'),
]

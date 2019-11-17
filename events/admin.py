from django.contrib import admin

# Register your models here.
from events.models import Event, Book, Room, Choice

admin.site.register(Event)
admin.site.register(Book)
admin.site.register(Room)
admin.site.register(Choice)

from django.contrib import admin
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from events import constants
from events.models import Event, Book, Room, Choice


# admin.site.register(Event)
# admin.site.register(Book)
# admin.site.register(Room)
# admin.site.register(Choice)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def applicant_info(self, obj):
        link = reverse('admin:applicants_applicant_change', args=[obj.applicant.id])
        return format_html('<a href="{}">{}</a>'.format(link, obj.applicant))

    applicant_info.short_description = 'Applicant'

    list_display = ('name', 'applicant_info', 'date', 'address',)
    list_filter = ('address', 'date',)
    ordering = ('address', 'date',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def get_accepted_count(self, obj):
        return obj.choices.filter(choice=constants.ACCEPTED).count()

    get_accepted_count.short_description = 'Accepted'

    def get_rejected_count(self, obj):
        return obj.choices.filter(choice=constants.REJECTED).count()

    get_rejected_count.short_description = 'Rejected'

    def get_confused_count(self, obj):
        return obj.choices.filter(choice=constants.CONFUSED).count()

    get_confused_count.short_description = 'Confused'

    list_display = ('name', 'date',
                    'get_accepted_count',
                    'get_rejected_count',
                    'get_confused_count')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'formatted_choice',)
    list_filter = ('event', 'choice',)

    def formatted_choice(self, obj):
        color = 'yellow'
        if obj.choice == constants.ACCEPTED:
            color = 'green'
        elif obj.choice == constants.REJECTED:
            color = 'red'
        return mark_safe(
            '<p style="color: white; background:{}; text-align: center;">{}</p>'.format(
                color, obj.get_choice_display()))

    formatted_choice.short_description = 'choice'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'nearest_book',)
    empty_value_display = 'There is no books for this room yet.'

    def nearest_book(self, obj):
        latest_book = obj.books.latest()
        if latest_book:
            link = reverse('admin:events_book_change', args=[latest_book.id])
            return format_html('<a href="{}">{} ({})</a>'.format(link,
                                                                 latest_book,
                                                                 latest_book.date.strftime("%H:%M %d.%m.%y")))
        return

    nearest_book.short_description = 'Nearest event'

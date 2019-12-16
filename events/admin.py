from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from events import constants
from events.models import Event, Book, Room, Choice


def format_for_user(obj, choice_type):
    choices = obj.choices.filter(choice=choice_type)
    html = "<div class='collapsible'><p>{}</p><ul>".format(choices.count())
    for choice in choices:
        link = reverse('admin:applicants_applicant_change', args=[choice.user.id])
        html += "<a href={}><li>{}</li></a>".format(link, choice.user)
    html += "</ul></div>"
    return mark_safe(html)


class BaseMixin:
    def get_model_info(self):
        app_label = self.model._meta.app_label
        return (app_label, self.model._meta.model_name)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def applicant_info(self, obj):
        link = reverse('admin:applicants_applicant_change', args=[obj.applicant.id])
        return format_html('<a href="{}">{}</a>'.format(link, obj.applicant))

    applicant_info.short_description = 'Applicant'

    list_display = ('name', 'applicant_info', 'date_begin', 'date_end', 'address',)
    list_filter = ('address', 'date_begin',)
    ordering = ('address',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/style.css',),
        }
        js = ('js/collapse.js',)

    def get_accepted_count(self, obj):
        return format_for_user(obj, constants.ACCEPTED)

    get_accepted_count.short_description = 'Accepted'

    def get_rejected_count(self, obj):
        return format_for_user(obj, constants.REJECTED)

    get_rejected_count.short_description = 'Rejected'

    def get_confused_count(self, obj):
        return format_for_user(obj, constants.CONFUSED)

    get_confused_count.short_description = 'Confused'

    def get_is_with_poll(self, obj):
        return obj.is_with_poll

    get_is_with_poll.short_description = 'Is with poll'
    get_is_with_poll.boolean = True

    list_display = ('name', 'date', 'get_is_with_poll',
                    'get_accepted_count',
                    'get_rejected_count',
                    'get_confused_count')

    fieldsets = (
        (None, {
            'fields': ('name', 'content', 'date', 'address',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('is_with_poll', 'deadline',),
        }),
    )


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin, BaseMixin):
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

    change_list_template = 'choice_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^notify/$',
                self.admin_site.admin_view(self.notify),
                name='%s_%s_notify' % self.get_model_info()),
        ]
        return my_urls + urls

    def notify(self, obj):
        return HttpResponseRedirect('../')

    list_display = ('user', 'event', 'formatted_choice',)
    list_filter = ('event', 'choice',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'nearest_book',)
    empty_value_display = 'There is no books for this room yet.'

    def nearest_book(self, obj):
        latest_book = obj.books.filter(date_begin__gte=timezone.now()).earliest()
        if latest_book:
            link = reverse('admin:events_book_change', args=[latest_book.id])
            return format_html('<a href="{}">{} ({})</a>'.format(link,
                                                                 latest_book,
                                                                 latest_book.date_begin.strftime("%H:%M %d.%m.%y")))
        return

    nearest_book.short_description = 'Nearest book'

from django.contrib import admin
# Register your models here.
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from applicants.forms import UpdateActionForm
from applicants.models import Applicant
from events import constants
from events.models import Event, Choice


def get_event_change_page(event):
    link = reverse('admin:events_event_change', args=[event.id])
    return '<a href="{}"><li>{}</li></a>'.format(link, event)


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/style.css',),
        }
        js = ('js/collapse.js',)

    action_form = UpdateActionForm
    exclude = ('user',)
    list_display = ('__str__', 'email', 'department', 'get_user_events')
    list_filter = ('department__name',)

    @transaction.atomic
    def send_event_notify(self, request, queryset):
        event_id = request.POST.get('event')
        event = get_object_or_404(Event, id=event_id)
        for obj in queryset:
            Choice.objects.get_or_create(user=obj.user, event=event)

    send_event_notify.short_description = _('Send notify to event.')

    def get_user_events(self, obj):
        q = obj.user.choices.exclude(choice=constants.REJECTED)
        html = "<div class='collapsible'><p>{}</p><ul>".format(q.count())
        for li in q:
            html += get_event_change_page(li.event)
        html += "</ul></div>"
        return mark_safe(html)

    get_user_events.short_description = _('User events')

    actions = ('send_event_notify',)

    search_fields = ['name', ]

    change_list_template = 'applicant_change.html'

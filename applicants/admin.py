from django.contrib import admin
# Register your models here.
from django.db import transaction
from django.shortcuts import get_object_or_404

from applicants.forms import UpdateActionForm
from applicants.models import Applicant
from events.models import Event, Choice


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    action_form = UpdateActionForm
    exclude = ('user',)
    list_display = ('__str__', 'email', 'department', 'get_user_events')
    list_filter = ('department__name',)

    @transaction.atomic
    def send_event_notify(self, request, queryset):
        event_id = request.POST.get('event')
        event = get_object_or_404(Event, id=event_id)
        for obj in queryset:
            Choice.objects.get_or_create(user=obj, event=event)
    send_event_notify.short_description = 'Send notify to event.'

    def get_user_events(self, obj):
        pass
    get_user_events.short_description = 'User events'

    actions = ('send_event_notify',)

    search_fields = ['name', ]

    change_list_template = 'applicant_change.html'


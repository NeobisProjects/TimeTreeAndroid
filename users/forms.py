from django import forms
from django.contrib.admin.helpers import ActionForm
from django.utils.timezone import now

from events.models import Event


class UpdateActionForm(ActionForm):
    event = forms.ModelChoiceField(Event.objects.filter(date__gte=now(), is_with_poll=True))

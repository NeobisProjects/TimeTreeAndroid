from django import forms
from django.contrib.admin.helpers import ActionForm

from events.models import Event


class UpdateActionForm(ActionForm):
    event = forms.ModelChoiceField(Event.objects.filter(is_with_poll=False))

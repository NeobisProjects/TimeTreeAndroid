from django.db.models.signals import post_save
from django.dispatch import receiver

from applicants.models import Applicant
from events.models import Event, Choice


@receiver(post_save, sender=Event)
def create_default_choices(sender, instance=None, created=False, **kwargs):
    if created:
        pass

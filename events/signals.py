from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Applicant
from events.models import Event, Choice
from events.services import Notifier


@receiver(post_save, sender=Event)
def create_default_choices(sender, instance=None, created=False, **kwargs):
    if created and not instance.is_with_poll:
        Notifier.notify_event_created(instance)

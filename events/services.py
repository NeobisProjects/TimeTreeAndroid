from django.utils.translation import ugettext_lazy as _
from fcm_django.models import FCMDevice

from events import constants
from events.models import Choice


class Notifier:
    @staticmethod
    def send_format_message(user, title, body):
        device = FCMDevice.objects.filter(user=user)
        if device.exists():
            device.send_message(str(title), str(body))

    @staticmethod
    def notify_confused():
        title = _('Event created')
        choices = Choice.objects.filter(choice=constants.CONFUSED)
        for choice in choices:
            try:
                body = _('Reply to this event: ') + str(choice.event)
                Notifier.send_format_message(choice.user, title, body)
            except:
                pass

    @staticmethod
    def notify_event_created(event):
        pass

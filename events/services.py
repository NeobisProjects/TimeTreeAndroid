from django.utils.translation import ugettext_lazy as _
from fcm_django.models import FCMDevice

from events import constants
from events.models import Choice


class Notifier:
    @staticmethod
    def send_format_message(user, title, body):
        if user is None:
            device = FCMDevice.objects.all()
        else:
            device = FCMDevice.objects.filter(user=user)

        if device.exists():
            device.send_message(str(title), str(body))

    @staticmethod
    def notify_confused():
        title = _('Event poll')
        choices = Choice.objects.filter(choice=constants.CONFUSED)
        for choice in choices:
            try:
                body = _('Reply to this event: ') + str(choice.event)
                Notifier.send_format_message(choice.user, title, body)
            except:
                pass

    @staticmethod
    def notify_event_created(event):
        title = _('Event created')
        try:
            body = _('Event created: ') + str(event)
            Notifier.send_format_message(None, title, body)
        except:
            pass

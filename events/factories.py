import factory
from django.utils import timezone

from events.models import Event, Room


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = 'Hackathon'
    content = 'Some useful content, just for test...'
    date = timezone.now()
    deadline = timezone.now()-timezone.timedelta(days=10)
    address = 'Baker st. 221b'


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    name = 'Coworking'
    location = 'Sport station'


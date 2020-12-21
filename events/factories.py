import factory
from django.utils import timezone

from users.factories import ApplicantFactory
from events import constants
from events.models import Event, Room, Choice


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


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

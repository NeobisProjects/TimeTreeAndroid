from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from applicants.factories import ApplicantFactory
from applicants.models import Applicant
from events import constants
from events.factories import RoomFactory, EventFactory, ChoiceFactory
from events.models import Choice, Event, Book, Room


class EventTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.room = RoomFactory()
        self.event = EventFactory()
        self.applicant = ApplicantFactory()
        self.user = User.objects.get(username='test@test.com')
        self.user.set_password('test_password')
        self.user.save()
        self.client.login(username="test@test.com", password="test_password")

    def test_event_created(self):
        self.second_applicant = ApplicantFactory(email='test@foo.bar')
        self.data = {
            "name": "Meetup",
            "content": "Some text for test.",
            "date": timezone.now(),
            "deadline": timezone.now()-timezone.timedelta(days=10),
            "address": "Unknown"
        }

        self.response = self.client.post(reverse('events:event_list'), self.data, format='json')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(Event.objects.filter(name='Meetup')[0]), self.data.get('name'))

    def test_book_creation(self):
        self.data = {
            "address": self.room.id,
            "date": timezone.now(),
            "name": "Backend meetup",
        }
        self.book = self.client.post(reverse('events:book_room'), self.data, format='json')
        self.assertEqual(self.book.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(Book.objects.filter(name='Backend meetup')[0], Book)

    def test_user_want_to_event(self):
        self.data = {
            "event": self.event.id,
            "choice": constants.ACCEPTED,
        }

        self.choice = self.client.post(reverse('events:set_choice'), self.data, format='json')
        self.assertEqual(self.choice.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(Choice.objects.filter(event=self.event.id)[0], Choice)
        self.assertEqual(len(Choice.objects.filter(choice=constants.ACCEPTED)), 1)
        self.assertEqual(len(Choice.objects.filter(choice=constants.REJECTED)), 0)

    def test_user_doesnt_want_to_event(self):
        self.data = {
            "event": self.event.id,
            "choice": constants.REJECTED
        }

        self.choice = self.client.post(reverse('events:set_choice'), self.data, format='json')
        self.assertEqual(self.choice.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Choice.objects.filter(choice=constants.REJECTED)), 1)
        self.assertEqual(len(Choice.objects.filter(choice=constants.ACCEPTED)), 0)

    def test_room_created(self):
        self.assertIsInstance(Room.objects.filter(name='Coworking')[0], Room)

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from applicants.factories import ApplicantFactory


class EventTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.applicant = ApplicantFactory()
        self.user = User.objects.filter(username=self.applicant.email).first()
        self.user.set_password("test_password")
        self.user.is_active = True
        self.user.save()

        self.client.login(username="test@test.com", password="test_password")
        self.data = {
            "participants": [self.applicant.id],
            "name": "Meetup",
            "content": "Some text for test.",
            "date": timezone.now(),
            "address": "Unknown"
        }

        self.response = self.client.post("/events/", self.data, format='json')

    def test_event_created(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

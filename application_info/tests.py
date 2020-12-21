from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIClient

from users.factories import ApplicantFactory


class AuxiliaryTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.applicant = ApplicantFactory()
        self.department = self.applicant.department

        self.user = User.objects.filter(username=self.applicant.email).first()
        self.user.set_password("test_password")
        self.user.is_active = True
        self.user.save()

        self.client.login(username="test@test.com", password="test_password")

        self.data = self.client.get(reverse('application_info:get_info'))

    def test_created_departments(self):
        self.assertContains(self.data, self.department)

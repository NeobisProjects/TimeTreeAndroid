from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from rest_framework.test import APIClient

from applicants.factories import ApplicantFactory
from applicants.models import Applicant
from application_info.factories import DepartmentFactory, UniversityFactory
from application_info.models import Department, University


class AuxiliaryTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.applicant = ApplicantFactory()
        self.department = self.applicant.department
        self.university = self.applicant.university

        self.user = User.objects.filter(username=self.applicant.email).first()
        self.user.set_password("test_password")
        self.user.is_active = True
        self.user.save()

        self.client.login(username="test@test.com", password="test_password")

        self.data = self.client.get("/values/")

    def test_created_departments_and_universities(self):
        self.assertContains(self.data, self.department)
        self.assertContains(self.data, self.university)

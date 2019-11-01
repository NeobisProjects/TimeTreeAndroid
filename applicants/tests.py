from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from rest_framework import status
from rest_framework.test import APIClient

from application_info.factories import DepartmentFactory, UniversityFactory


class ApplicantTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.department = DepartmentFactory()
        self.university = UniversityFactory()

        self.user_data = {
            "name": "Vladimir",
            "surname": "Putin",
            "email": "test@test.com",
            "department": self.department.id,
            "university": self.university.id
        }
        self.values = self.client.get("/values/")

        self.user = self.client.post("/applicants/", data=self.user_data, format='json')
        self.check_user = User.objects.filter(username="test@test.com").first()
        self.check_user.set_password("test_password")
        self.check_user.save()

    def test_create_user(self):
        self.assertEqual(self.user.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.check_user)

    def test_can_view_info(self):
        self.client.login(username="test@test.com", password="test_password")
        self.values = self.client.get("/values/")
        self.assertEqual(self.values.status_code, status.HTTP_200_OK)

    def test_cannot_view_info(self):
        self.assertEqual(self.values.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_change_password(self):
        self.client.post("/applicants/login", data={"email": "test@test.com", "password": "test_password"},
                         format='json')
        self.change_password_data = {
            "old_password": "test_password",
            "new_password": "very_strong_password",
            "new_password_check": "very_strong_password"
        }
        self.change_status = self.client.post("/applicants/change_password", data=self.change_password_data,
                                              format='json')
        self.assertEqual(self.change_status.status_code, status.HTTP_200_OK)

    def test_can_change_wrong_password(self):
        self.client.post("/applicants/login", data={"email": "test@test.com", "password": "test_password"},
                         format='json')
        self.change_password_data = {
            "old_password": "test_passwor",
            "new_password": "very_strong_password",
            "new_password_check": "very_strong_password"
        }
        self.change_status = self.client.post("/applicants/change_password", data=self.change_password_data,
                                              format='json')
        self.assertEqual(self.change_status.status_code, status.HTTP_400_BAD_REQUEST)

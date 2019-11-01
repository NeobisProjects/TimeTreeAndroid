import factory

from applicants.models import Applicant
from application_info.factories import DepartmentFactory, UniversityFactory


class ApplicantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Applicant

    name = "Vladimir"
    surname = "Putin"
    email = "test@test.com"
    department = factory.SubFactory(DepartmentFactory)
    university = factory.SubFactory(UniversityFactory)

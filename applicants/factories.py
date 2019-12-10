import factory

from applicants.models import Applicant
from application_info.factories import DepartmentFactory


class ApplicantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Applicant
        django_get_or_create = ('email',)

    name = "User"
    surname = factory.sequence(lambda x: "%d" % x)
    email = "test@test.com"
    department = factory.SubFactory(DepartmentFactory)

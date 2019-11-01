from factory.django import DjangoModelFactory

from application_info.models import Department, University


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = "Backend"


class UniversityFactory(DjangoModelFactory):
    class Meta:
        model = University

    name = "Hogwarts"
    city = "Scotland"

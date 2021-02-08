from factory.django import DjangoModelFactory

from application_info.models import Department


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = "Backend"

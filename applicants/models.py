from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from application_info.models import Department, University


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(max_length=20, unique=True)
    department = models.ForeignKey(Department,
                                   verbose_name=_('User\'s department'),
                                   related_name='users_department',
                                   on_delete=models.PROTECT)
    university = models.ForeignKey(University,
                                   verbose_name=_('User\'s university'),
                                   related_name='users_university',
                                   on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} {self.surname}'

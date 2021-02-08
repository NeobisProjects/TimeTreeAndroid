from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from application_info.models import Department


class Applicant(models.Model):
    user = models.OneToOneField(User, related_name='applicant', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    surname = models.CharField(max_length=100, verbose_name=_('Surname'))
    email = models.EmailField(max_length=100, unique=True, verbose_name=_('Email'))
    department = models.ForeignKey(Department,
                                   verbose_name=_('User\'s department'),
                                   related_name='users_department',
                                   on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)

    class Meta:
        verbose_name = _('Applicant')
        verbose_name_plural = _('Applicants')

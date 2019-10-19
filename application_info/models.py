from django.db import models
from django.utils.translation import gettext_lazy as _


class University(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    city = models.CharField(max_length=20, verbose_name=_('City'))

    class Meta:
        verbose_name = _('University')
        verbose_name_plural = _('Universities')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return self.name



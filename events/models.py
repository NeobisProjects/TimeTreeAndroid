from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from events import constants


class Event(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    content = models.TextField(max_length=500, verbose_name=_('Content'))
    date = models.DateTimeField(verbose_name=_('Date'))
    address = models.CharField(max_length=100, verbose_name=_('Address'))
    is_with_poll = models.BooleanField(default=False, verbose_name=_('Is with poll'))
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_('Deadline'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def get_time(self):
        return self.date.time()

    @property
    def get_date(self):
        return self.date.date()

    @property
    def get_choice(self):
        if self.choices.exists():
            return self.choices.first().choice
        return None


class Choice(models.Model):
    event = models.ForeignKey(Event, related_name='choices', on_delete=models.CASCADE, verbose_name=_('Event'))
    user = models.ForeignKey(User, related_name='choices', on_delete=models.CASCADE, verbose_name=_('Applicant'))
    choice = models.IntegerField(choices=constants.choices, default=constants.CONFUSED, verbose_name=_('Choice'))

    class Meta:
        unique_together = ['event', 'user']
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')

    def __str__(self):
        return "{}".format(self.user)


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    location = models.CharField(max_length=255, verbose_name=_('Location'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')


class Book(models.Model):
    applicant = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE, verbose_name=_('Applicant'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    date_begin = models.DateTimeField(verbose_name=_('Date begin'))
    date_end = models.DateTimeField(verbose_name=_('Date end'))
    address = models.ForeignKey(Room, related_name='books', on_delete=models.CASCADE, verbose_name=_('Address'))

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ('date_begin',)
        get_latest_by = ('date_begin',)
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    @property
    def get_date_begin(self):
        return self.date_begin.date()

    @property
    def get_time_begin(self):
        return self.date_begin.time()

    @property
    def get_date_end(self):
        return self.date_end.date()

    @property
    def get_time_end(self):
        return self.date_end.time()

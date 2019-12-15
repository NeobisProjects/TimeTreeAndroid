import datetime

from django.contrib.auth.models import User
from django.db import models

from applicants.models import Applicant
from events import constants


class Event(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    date = models.DateTimeField()
    address = models.CharField(max_length=100)
    is_with_poll = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)

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
        return self.choices.first().choice


class Choice(models.Model):
    event = models.ForeignKey(Event, related_name='choices', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='choices', on_delete=models.CASCADE)
    choice = models.IntegerField(choices=constants.choices, default=constants.CONFUSED)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return "{}".format(self.user)


class Room(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)


class Book(models.Model):
    applicant = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    address = models.ForeignKey(Room, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ('date_begin',)
        get_latest_by = ('date_begin',)

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

import datetime

from django.db import models

from applicants.models import Applicant
from events import constants


class Event(models.Model):
    participants = models.ManyToManyField(Applicant, related_name='users_events')
    name = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    date = models.DateTimeField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)


class Choice(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(Applicant, related_name='choice', on_delete=models.CASCADE)
    choice = models.IntegerField(choices=constants.choices, default=constants.UNCERTAIN)

    def __str__(self):
        return "{} {}".format(self.user, self.choice)


class Room(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)


class Book(models.Model):
    applicant = models.ForeignKey(Applicant, related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(unique=True)
    address = models.ForeignKey(Room, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.date.strftime("%d %a. %H %M"))

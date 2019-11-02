import datetime

from django.db import models

from applicants.models import Applicant


class Event(models.Model):
    participants = models.ManyToManyField(Applicant, related_name='users_events')
    name = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    date = models.DateTimeField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Choice(models.Model):
    UNCERTAIN = 1
    PARTICIPATE = 2
    NON_PARTICIPATE = 3

    choices = (
        (UNCERTAIN, 'Uncertain'),
        (PARTICIPATE, 'Participant'),
        (NON_PARTICIPATE, 'Non_participate')
    )

    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    user = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    choice = models.IntegerField(choices=choices, default=UNCERTAIN)


class Book(models.Model):
    applicant = models.ForeignKey(Applicant, related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(unique_for_date=True)
    address = models.CharField(max_length=100)
    period = models.DurationField()

    def __str__(self):
        return f'{self.name} - {self.date.strftime("%d %a. %H %M")} for {self.period}'

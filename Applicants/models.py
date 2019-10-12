from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} {self.surname}'

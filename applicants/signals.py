from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from applicants.models import Applicant


# @receiver(pre_save, sender=User)
# def change_user_active(sender, instance, **kwargs):
#     if instance._state.adding and not instance.is_superuser:
#         instance.is_active = False


@receiver(pre_save, sender=Applicant)
def create_applicant_with_user(sender, instance, **kwargs):
    print(*["=" for _ in range(20)], sep="", end='\n')
    print('Before user object create')
    user = User.objects.create_user(username=instance.email, email=instance.email)
    instance.user = user
    print('After user create')
    print(*["=" for _ in range(20)], sep="", end='\n')


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


@receiver(post_delete, sender=Applicant)
def delete_related_user(sender, instance, **kwargs):
    User.objects.filter(username=instance.email).delete()

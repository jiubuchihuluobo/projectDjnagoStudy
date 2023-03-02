from django.db.models.signals import post_save
from django.dispatch import receiver

from customauth.models import User
from todoapp.models import Profile


# post_save方法会在create与save后调用
@receiver(signal=post_save, sender=User)
def create_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


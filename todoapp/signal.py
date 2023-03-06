import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from todoapp.models import Profile


@receiver(pre_delete, sender=Profile)
def avatar_delete(instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path) and "profile_avatars" in instance.avatar.path:
            os.remove(instance.avatar.path)

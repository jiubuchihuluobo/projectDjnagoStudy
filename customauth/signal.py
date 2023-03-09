from django.db.models.signals import post_save
from django.dispatch import receiver

from customauth.models import User
from todoapp.models import Profile


# @receiver装饰器为隐式调用
# 信号post_save会在create与save后调用
@receiver(signal=post_save, sender=User, dispatch_uid="84a7caf43f98408a98eb5aa2f0e17d8f")
def create_profile(instance, created, **kwargs):
    # 参数created等于True代表创建
    if created:
        Profile.objects.create(user=instance)

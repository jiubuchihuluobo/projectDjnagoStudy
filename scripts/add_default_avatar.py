import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'permissionTest.settings')
django.setup()

from customauth.models import User
from todoapp.models import Profile

for user in User.objects.all():
    try:
        user.profile
    except Exception as e:

        Profile.objects.create(user=user, avatar="avatar.jpg")
        print("创建头像")

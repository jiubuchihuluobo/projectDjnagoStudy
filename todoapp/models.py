import os

from PIL import Image
from django.db import models

from customauth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['completed']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.jpg', upload_to='profile_avatars')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        self.__class__.objects.filter(user__exact=self.user).delete()
        super().save(*args, **kwargs)
        if os.path.isfile(self.avatar.path):
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300 or img.height < 300 or img.width < 300:
                output_size = (300, 300)
                # 创建缩略图
                img.thumbnail(output_size)
                img.save(self.avatar.path)

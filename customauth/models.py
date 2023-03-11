from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64, help_text="标签名字")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 正数或0
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class User(AbstractUser):
    tags = GenericRelation(Tag, related_query_name="user")

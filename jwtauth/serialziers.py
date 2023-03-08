from django.contrib.auth import models
from rest_framework import relations
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from customauth.models import User


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    groups = relations.PrimaryKeyRelatedField(
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        many=True,
        queryset=models.Group.objects.all(),
        required=False
    )
    user_permissions = relations.PrimaryKeyRelatedField(
        help_text='Specific permissions for this user.',
        many=True,
        queryset=models.Permission.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = "__all__"


class MyTokenObtainPairSerializer(UserSerializer, TokenObtainPairSerializer):
    # 登陆不需要二次密码确认
    password_confirm = None

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

    def validate(self, attrs):
        token_data = super().validate(attrs)

        # 欺骗serializer完成了is_valid
        self._validated_data = {}
        self.instance = self.user
        user_data = self.data

        # 合并token信息与user信息
        merge_data = {**user_data, **token_data}

        return merge_data

    def create(self, validated_data):
        ...

    def update(self, instance, validated_data):
        ...

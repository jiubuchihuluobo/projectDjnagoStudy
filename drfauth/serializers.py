from django.contrib.auth import validators
from django.urls import reverse
from django.utils.translation import gettext_lazy
from rest_framework import serializers
from rest_framework.fields import IntegerField, CharField, DateTimeField, BooleanField, EmailField
from rest_framework.validators import UniqueValidator

from customauth.models import User


class UserSerializer(serializers.Serializer):
    id = IntegerField(label='ID', read_only=True)

    password = CharField(max_length=128, write_only=True)
    confirm = CharField(max_length=128, write_only=True)

    last_login = DateTimeField(allow_null=True, required=False)
    is_superuser = BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', label='Superuser status', required=False)
    first_name = CharField(allow_blank=True, max_length=150, required=False)
    last_name = CharField(allow_blank=True, max_length=150, required=False)
    email = EmailField(allow_blank=True, label='Email address', max_length=254, required=False)
    is_staff = BooleanField(help_text='Designates whether the user can log into this admin site.', label='Staff status', required=False)
    is_active = BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', label='Active', required=False)
    date_joined = DateTimeField(required=False)

    # 处理验证字段
    username = CharField(
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        max_length=150,
        validators=[validators.UnicodeUsernameValidator(), UniqueValidator(queryset=User.objects.all())]
    )

    # 处理关系字段
    # groups = PrimaryKeyRelatedField(
    #     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    #     many=True,
    #     queryset=Group.objects.all(),
    #     required=False
    # )
    # user_permissions = PrimaryKeyRelatedField(
    #     help_text='Specific permissions for this user.',
    #     many=True,
    #     queryset=Permission.objects.all(),
    #     required=False
    # )

    # 处理关系字段
    groups = serializers.StringRelatedField(
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        many=True,
        # queryset=Group.objects.all(),
        required=False,
    )
    user_permissions = serializers.StringRelatedField(
        help_text='Specific permissions for this user.',
        many=True,
        # queryset=Permission.objects.all(),
        required=False,
    )

    # validate可以自定义验证
    # validate可以编写视图函数的逻辑
    def validate(self, attrs):
        # 注册逻辑
        if reverse("drfauth:register") == self.context.get("request").path:
            if attrs["password"] != attrs.pop("confirm"):
                msg = gettext_lazy('两次输入的密码不一致')
                raise serializers.ValidationError(msg, code='authorization')
        return attrs

    def update(self, instance, validated_data: dict):
        raise NotImplementedError('`update()` must be implemented.')

    # 在create方法中删除无用的数据用来保存
    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        return user


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Creating a ModelSerializer without either the 'fields' attribute or the 'exclude' attribute has been deprecated since 3.3.0, and is now disallowed. Add an explicit fields = '__all__' to the UserModelSerializer serializer.
        fields = '__all__'

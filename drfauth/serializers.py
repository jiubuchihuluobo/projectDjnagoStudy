from django.contrib.auth import validators
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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

    username = CharField(
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        max_length=150,
        validators=[validators.UnicodeUsernameValidator(), UniqueValidator(queryset=User.objects.all())]
    )

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

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data: dict):
        if validated_data.pop("confirm") == validated_data.get("password"):
            user = User.objects.create_user(**validated_data)
        else:
            raise ValidationError("两次密码输入不一致")
        return user


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Creating a ModelSerializer without either the 'fields' attribute or the 'exclude' attribute has been deprecated since 3.3.0, and is now disallowed. Add an explicit fields = '__all__' to the UserModelSerializer serializer.
        fields = '__all__'

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

    def is_valid(self, *, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                # 原始
                self._validated_data = self.run_validation(self.initial_data)

                # 注册
                if (not self.context.get("request")) and (self._validated_data["password"] != self._validated_data.pop("confirm")):
                    raise ValidationError("Password confirm error")

                # 登陆
                # if self.context.get("request") and self._validated_data.pop("password") == "":
                #     self.instance = authenticate(
                #         self.context.get("request"),
                #         username=self._validated_data["username"],
                #         password=self._validated_data["password"],
                #     )
                #     if not self.instance:
                #         raise ValidationError("Password input error")
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        return user


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Creating a ModelSerializer without either the 'fields' attribute or the 'exclude' attribute has been deprecated since 3.3.0, and is now disallowed. Add an explicit fields = '__all__' to the UserModelSerializer serializer.
        fields = '__all__'

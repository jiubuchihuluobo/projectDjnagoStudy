from collections import OrderedDict
from collections.abc import Mapping

from django.contrib.auth import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers, relations
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField, get_error_detail, set_value
from rest_framework.relations import PKOnlyObject
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from customauth.models import User, Tag


class OutstandingTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutstandingToken
        fields = ["id", "jti", "created_at", "expires_at"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaggedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Tag):
            serializer = TagSerializer(instance=value)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    # 模型类关系字段related_name未设置时，嵌套关系字段名字一定是反向模型类小写名字下划线set
    # outstandingtoken_set = OutstandingTokenSerializer(many=True, read_only=True)

    password_confirm = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    groups = relations.PrimaryKeyRelatedField(
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        many=True,
        queryset=models.Group.objects.all(),
        required=False,
    )

    user_permissions = relations.PrimaryKeyRelatedField(
        help_text='Specific permissions for this user.',
        many=True,
        queryset=models.Permission.objects.all(),
        required=False,
    )

    # 自动生成的，反向关系必须在fields中直接声明，__all__并不会生成反向关系序列化字段
    outstandingtoken_set = OutstandingTokenSerializer(
        many=True,
        read_only=True,
    )

    tags = TaggedObjectRelatedField(
        many=True,
        required=False,
        queryset=Tag.objects.filter(content_type=ContentType.objects.get_for_model(model=User)),
        validators=[UniqueValidator(queryset=ContentType.objects.get_for_model(model=User))],
    )

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):

        # 注册
        if "register" in self.context["request"].path_info and \
                attrs.get("password") != attrs.pop("password_confirm"):
            return serializers.ValidationError(detail="两次输入的密码不一致")

        return attrs

    def create(self, validated_data):
        credentials = {
            "username": validated_data.get("username"),
            "password": validated_data.get("password"),
        }
        self.instance = self.Meta.model.objects.create_user(**credentials)
        return self.instance

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:

            # 登陆或更新
            if ("login" in self.context.get("request").path_info or self.context.get("request").method == "PUT") and \
                    field.field_name == "outstandingtoken_set":
                continue

            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields

        for field in fields:

            # 更新
            if self.context.get("request").method == "PUT" and \
                    "user_info" in self.context.get("request").path_info and \
                    (field.field_name == 'password' or field.field_name == "password_confirm"):
                continue

            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                errors[field.field_name] = exc.detail
            except DjangoValidationError as exc:
                errors[field.field_name] = get_error_detail(exc)
            except SkipField:
                pass
            else:
                set_value(ret, field.source_attrs, validated_value)

        if errors:
            raise ValidationError(errors)

        return ret


class MyTokenObtainPairSerializer(TokenObtainPairSerializer, UserSerializer):
    # 跳过校验
    password_confirm = serializers.SkipField()

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

    def validate(self, attrs):
        token_data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        # 欺骗serializer完成了is_valid
        self._validated_data = {}
        self.instance = self.user
        user_data = self.data

        # 合并token信息与user信息
        merge_data = {**user_data, **token_data}

        return merge_data

    def update(self, instance, validated_data):
        ...

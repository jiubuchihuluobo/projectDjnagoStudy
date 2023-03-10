from django.contrib.auth import models
from rest_framework import serializers, relations
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
        pass

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
        read_only=True,
    )

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get("password") != attrs.pop("password_confirm"):
            return serializers.ValidationError(detail="两次输入的密码不一致")
        return attrs

    def create(self, validated_data):
        credentials = {
            "username": validated_data.get("username"),
            "password": validated_data.get("password"),
        }
        self.instance = self.Meta.model.objects.create_user(**credentials)
        return self.instance


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

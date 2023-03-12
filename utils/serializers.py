from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from jwtauth.serialziers import GeneralUserSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer, GeneralUserSerializer):
    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

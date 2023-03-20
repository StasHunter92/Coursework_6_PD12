from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, \
    UserSerializer as BaseUserSerializer, SetPasswordSerializer
from django.contrib.auth import get_user_model

# ----------------------------------------------------------------------------------------------------------------------
# Get user model from project
User = get_user_model()


# ----------------------------------------------------------------------------------------------------------------------
# User serializers
class UserSerializer(BaseUserSerializer):
    """
    Serializer for List and Retrieve view
    """

    class Meta:
        model: User = User
        fields: list[str] = ['first_name', 'last_name', 'phone', 'id', 'email', 'image']
        read_only_fields = ['id', 'email']


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for Create view
    """
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model: User = User
        fields: list[str] = ['email', 'first_name', 'last_name', 'password', 'phone', 'image']


class UserPasswordChangeSerializer(SetPasswordSerializer):
    """
    Serializer for PasswordChange view
    """
    current_password = serializers.CharField(style={'input_type': 'password'})
    new_password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model: User = User
        fields: list[str] = ['new_password', 'current_password']

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

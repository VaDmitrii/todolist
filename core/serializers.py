from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from core.fields import PasswordField
from core.models import User


class CoreSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_repeat']

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError('passwords must match')
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'email',)

    def create(self, validated_data: dict) -> User:
        if user := authenticate(
                username=validated_data['username'],
                password=validated_data['password']
        ):
            return user
        raise AuthenticationFailed


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate_password(self, old_password: str) -> str:
        if not self.instance.check_password(old_password):
            raise ValidationError('password is incorrect')
        return old_password

    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username',)

from rest_framework import serializers
from .models import Registration
from django.contrib.auth.models import User


class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        extra_kwargs = {
            'password1': {
                'write_only': True
            },
            'password2': {
                'write_only': True
            }
        }


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class EmailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email'
        ]


class ResetSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'password'
        ]

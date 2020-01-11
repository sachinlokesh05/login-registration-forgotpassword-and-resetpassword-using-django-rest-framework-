from rest_framework import serializers
from .models import Registration
from django.contrib.auth.models import User


class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]


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

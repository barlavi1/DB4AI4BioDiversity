from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, value: str):
        return make_password(value)


class TokenObtainPairWithData(TokenObtainPairSerializer):
    def validate(self, attrs):
        # validate credentials of the POST request
        data = super().validate(attrs)
        data['lifetime'] = int(settings.__dict__["SIMPLE_JWT"]["ACCESS_TOKEN_LIFETIME"].total_seconds())
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['email'] = self.user.email
        return data


class TokenRefreshWithData(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['lifetime'] = int(settings.__dict__["SIMPLE_JWT"]["ACCESS_TOKEN_LIFETIME"].total_seconds())
        return data

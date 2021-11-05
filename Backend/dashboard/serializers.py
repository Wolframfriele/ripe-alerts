from typing_extensions import ParamSpecKwargs
from django.db import IntegrityError
from django.db.models import fields
from django.contrib.auth.models import User
from django.db.models.base import Model
from rest_framework import serializers
from .models import AlertConfiguration, RipeUser
from .ripe_api import is_token_valid


class UserSerializer(serializers.ModelSerializer):
    ripe_api_token = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['username', 'ripe_api_token']


class TokenNotValid(Exception):
    """Exception raised for error in the token.

    Attributes:
        token -- input token which caused the error
        message -- explanation of the error
    """

    def __init__(self, token):
        self.token = token
        self.message = "token not valid"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.token} -> {self.message}'


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    ripe_api_token = serializers.UUIDField(required=False)

    def create(self, validated_data: dict):
        """
        Create a new user and associated api-token record, given the validated data.
        """
        ripe_api_token = validated_data.get('ripe_api_token', None)
        if ripe_api_token is not None and is_token_valid(ripe_api_token) is False:
            raise TokenNotValid(ripe_api_token)
        try: 
            user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        except IntegrityError:
            raise IntegrityError

        ripe_user = RipeUser(user=user, ripe_api_token=ripe_api_token)
        ripe_user.save()
        return user

    def update(self, instance, validated_data):
        pass


class TokenSerializer(serializers.Serializer):
    pass


class AlertConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertConfiguration
        fields = '__all__' 


class TargetSerializer(serializers.Serializer):
    ip_v4 = serializers.CharField(required=False)
    ip_v6 = serializers.CharField(required=False)
    ip = serializers.CharField(required=False)
    host = serializers.CharField(required=False)

    def validate(self, data):
        """
        Check that at least one ip is given
        """

        if not data.get('ip_v4') and not data.get('ip_v6') and not data.get('ip') and not data.get('host'):
            raise serializers.ValidationError("we need at least input for ip_v4, ip_v6, ip or host")
        return data

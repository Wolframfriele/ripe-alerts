from typing_extensions import ParamSpecKwargs
from django.db import IntegrityError
from django.db.models import fields
from django.contrib.auth.models import User
from django.db.models.base import Model
from rest_framework import serializers
from .models import AlertConfiguration, RipeUser


class UserSerializer(serializers.ModelSerializer):
    ripe_api_token = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ['id', 'username', 'ripe_api_token']

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    ripe_api_token = serializers.UUIDField(required=False)

    def create(self, validated_data: dict):
        """
        Create a new user and associated api-token record, given the validated data.
        """
        try: 
            user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        except IntegrityError:
            raise IntegrityError

        ripe_user = RipeUser(user=user, ripe_api_token=validated_data.get('ripe_api_token', None))
        ripe_user.save()
        return user


class AlertConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertConfiguration
        fields = '__all__' 

from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import RipeUser
from .services import InitialSetupService
from ripe_atlas.exceptions import TokenNotValid
from ripe_atlas.serializers import TargetSerializer, AnchorSerializer
from ripe_atlas.interfaces import RipeInterface
from ripe_atlas.models import System, Measurement
from alert_configuration.models import AlertConfiguration


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    ripe_api_token = serializers.UUIDField(required=True,)

    def create(self, validated_data: dict):
        """
        Create a new user and associated api-token record, given the validated data.
        """
        ripe_api_token = validated_data['ripe_api_token']
        if RipeInterface.is_token_valid(ripe_api_token) is False:
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


class InitialSetupSerializer(serializers.Serializer):
    targets = TargetSerializer(many=True)
    anchors = AnchorSerializer(many=True)
    email = serializers.CharField(max_length=100)

    def validate(self, data):
        if len(data['targets']) == 0 and len(data['anchors']) == 0:
            raise serializers.ValidationError("we need at least an target or anchor for the initial setup")
        return data

    def create(self, validated_data):
        return InitialSetupService.store_initial_setup(validated_data)





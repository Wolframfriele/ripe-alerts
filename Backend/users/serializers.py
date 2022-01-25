from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import RipeUser
from .services import InitialSetupService
from ripe_atlas.exceptions import TokenNotValid
from ripe_atlas.interfaces import RipeInterface


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
    asns = serializers.ListField(child=serializers.CharField(max_length=100, required=True))
    email = serializers.CharField(max_length=100, required=True)

    def validate(self, data):
        anchors_by_asn = RipeInterface.get_anchors(data['asns'])
        if not anchors_by_asn:
            raise serializers.ValidationError("No anchors found with ASN")
        data['anchors_by_asn'] = anchors_by_asn
        return data

    def create(self, validated_data):
        return InitialSetupService.store_initial_setup(validated_data)

    def update(self, instance, validated_data):
        pass





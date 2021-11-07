from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import RipeUser
from ripe_atlas.exceptions import TokenNotValid
from ripe_atlas.ripe_api import is_token_valid


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    ripe_api_token = serializers.UUIDField(required=True,)

    def create(self, validated_data: dict):
        """
        Create a new user and associated api-token record, given the validated data.
        """
        ripe_api_token = validated_data['ripe_api_token']
        if is_token_valid(ripe_api_token) is False:
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



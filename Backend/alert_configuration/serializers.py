from typing_extensions import ParamSpecKwargs
from django.db import IntegrityError
from django.db.models import fields
from django.contrib.auth.models import User
from django.db.models.base import Model
from rest_framework import serializers
from .models import AlertConfiguration
from users.models import RipeUser
from ripe_atlas.exceptions import TokenNotValid
from ripe_atlas.interfaces import is_token_valid


class AlertConfigurationSerializer(serializers.Serializer):
    # alert_configuration_id = models.AutoField(primary_key=True)
    # measurement_id = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    # alert_configuration_type = models.CharField(max_length=100)
    # alert_configuration = models.JSONField()
    pass




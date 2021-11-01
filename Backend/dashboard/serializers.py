from typing_extensions import ParamSpecKwargs
from django.db.models import fields
from rest_framework import serializers
from .models import AlertConfiguration

class AlertConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertConfiguration
        fields = '__all__' 
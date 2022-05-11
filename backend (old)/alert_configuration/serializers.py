from rest_framework import serializers
from .models import Anomaly


class AnomalySerializer(serializers.ModelSerializer):
    class Meta:
        model = Anomaly
        exclude = ['alert_configuration']






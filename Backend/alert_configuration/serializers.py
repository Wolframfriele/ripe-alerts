from rest_framework import serializers
from .models import Anomaly


class AnomalySerializer(serializers.ModelSerializer):
    class Meta:
        model = Anomaly
        exclude = ['alert_configuration']


class AlertConfigurationSerializer(serializers.Serializer):
    # alert_configuration_id = models.AutoField(primary_key=True)
    # measurement_id = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    # alert_configuration_type = models.CharField(max_length=100)
    # alert_configuration = models.JSONField()
    pass




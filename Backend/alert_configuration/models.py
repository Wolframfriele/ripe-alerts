from django.db import models
from django.contrib.auth.models import User
from ripe_atlas.models import Measurement
import time


class AlertConfiguration(models.Model):
    alert_configuration_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    alert_configuration_type = models.CharField(max_length=100)
    alert_configuration = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'measurement', 'alert_configuration_type'],
                                    name='unique_user_alert_configuration_on_measurement')
        ]


def current_unixtime():
    return int(time.time())


class Anomaly(models.Model):

    anomaly_id = models.AutoField(primary_key=True)
    alert_configuration = models.ForeignKey(AlertConfiguration, on_delete=models.CASCADE)
    description = models.TextField()
    label = models.BooleanField(null=True)
    datetime = models.BigIntegerField(default=current_unixtime)
    is_alert = models.BooleanField(default=False)

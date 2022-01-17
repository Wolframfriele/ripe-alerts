from django.db import models
from django.contrib.auth.models import User
import time


# Create your models here.
class RipeUser(models.Model):
    user = models.OneToOneField(User, related_name='ripe_user', on_delete=models.CASCADE)
    initial_setup_complete = models.BooleanField(default=False)
    ripe_api_token = models.UUIDField(null=False, blank=False)

    def __str__(self):
        return str(self.ripe_api_token)


class Asn(models.Model):
    asn = models.IntegerField(primary_key=True)


class Anchor(models.Model):

    anchor_id = models.IntegerField(primary_key=True)
    ip_v4 = models.CharField(max_length=128, blank=True, null=True, default=None, unique=True)
    ip_v6 = models.CharField(max_length=128, blank=True, null=True, default=None, unique=True)
    asn = models.ForeignKey(Asn, on_delete=models.CASCADE)
    fqdn = models.CharField(max_length=200, blank=True, null=True, default=None)


class Measurement(models.Model):
    class MeasurementType(models.TextChoices):
        PING = 'ping'
        TRACEROUTE = 'traceroute'
        DNS = 'dns'
        SSLCERT = 'sslcert'
        HTTP = 'http'
        NTP = 'ntp'

    measurement_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=10, choices=MeasurementType.choices, null=False)
    interval = models.IntegerField(null=False)
    anchor = models.ForeignKey(Anchor, on_delete=models.CASCADE)


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

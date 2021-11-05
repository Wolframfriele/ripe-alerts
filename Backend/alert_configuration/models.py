from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.


class Target(models.Model):
    target_id = models.IntegerField(primary_key=True)
    probe_id = models.IntegerField(unique=True)
    prefix_v4 = models.CharField(max_length=128, blank=True, default="")
    prefix_v6 = models.CharField(max_length=128, blank=True, default="")
    ip_v4 = models.CharField(max_length=128, blank=True, default="")
    ip_v6 = models.CharField(max_length=128, blank=True, default="")
    asn_v4 = models.CharField(max_length=128, blank=True, default="")
    asn_v6 = models.CharField(max_length=128, blank=True, default="")
    host = models.CharField(max_length=200, blank=True, default="")


class Measurement(models.Model):
    class MeasurementType(models.TextChoices):
        PING = 'Ping'
        TRACEROUTE = 'Traceroute'
        DNS = 'Dns'
        SSLCERT = 'Sslcert'
        HTTP = 'Http'
        NTP = 'Ntp'

    measurement_id = models.IntegerField(primary_key=True)
    measurement_type = models.CharField(max_length=10, choices=MeasurementType.choices)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)


class AlertConfiguration(models.Model):
    alert_configuration_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    alert_configuration_type = models.CharField(max_length=100)
    alert_configuration = models.JSONField()


class Alert(models.Model):
    class Severity(models.TextChoices):
        WARNING = 'Warning'
        MINOR = 'Minor'
        MAJOR = 'Major'
        CRITICAL = 'Critical'

    alert_id = models.AutoField(primary_key=True)
    alert_configuration = models.ForeignKey(AlertConfiguration, on_delete=CASCADE)
    severity = models.CharField(max_length=10, choices=Severity.choices, default=Severity.CRITICAL)
    description = models.TextField()
    feedback = models.BooleanField(null=True)

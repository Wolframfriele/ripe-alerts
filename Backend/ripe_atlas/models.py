from django.db import models


class Target(models.Model):
    class TargetType(models.TextChoices):
        EXTERN = 'Extern'
        PROBE = 'Probe'

    target_id = models.AutoField(primary_key=True)
    target_type = models.CharField(max_length=10, choices=TargetType.choices, default=TargetType.PROBE)
    probe_id = models.IntegerField(unique=True)
    prefix_v4 = models.CharField(max_length=128, null=True, default=None)
    prefix_v6 = models.CharField(max_length=128, blank=True, null=True, default=None)
    address_v4 = models.CharField(max_length=128, blank=True, null=True, default=None)
    address_v6 = models.CharField(max_length=128, blank=True, null=True, default=None)
    asn_v4 = models.CharField(max_length=128, blank=True, null=True, default=None)
    asn_v6 = models.CharField(max_length=128, blank=True, null=True, default=None)
    host = models.CharField(max_length=200, blank=True, null=True, default=None)


class Measurement(models.Model):
    class MeasurementType(models.TextChoices):
        PING = 'ping'
        TRACEROUTE = 'traceroute'
        DNS = 'dns'
        SSLCERT = 'sslcert'
        HTTP = 'http'
        NTP = 'ntp'

    measurement_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=10, choices=MeasurementType.choices, null=False)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
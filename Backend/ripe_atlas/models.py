from django.db import models


class System(models.Model):
    class SystemType(models.TextChoices):
        TARGET = 'target'
        ANCHOR = 'anchor'

    system_ud = models.AutoField(primary_key=True)
    target_type = models.CharField(max_length=10, choices=SystemType.choices, default=SystemType.ANCHOR)
    probe_id = models.IntegerField(unique=True)
    prefix_v4 = models.CharField(max_length=128, null=True, default=None)
    prefix_v6 = models.CharField(max_length=128, blank=True, null=True, default=None)
    address_v4 = models.CharField(max_length=128, blank=True, null=True, default=None, unique=True)
    address_v6 = models.CharField(max_length=128, blank=True, null=True, default=None, unique=True)
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
    description = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=10, choices=MeasurementType.choices, null=False)
    system = models.ForeignKey(System, on_delete=models.CASCADE)

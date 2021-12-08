from django.db import models


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

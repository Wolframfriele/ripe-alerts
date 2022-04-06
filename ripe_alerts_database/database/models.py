# This class contains all entities which are later converted to tables by Django.
from enum import Enum
from django.db import models
from django.contrib.auth.models import User


class MeasurementType(models.TextChoices):
    PING = 'Ping'
    TRACEROUTE = 'Traceroute'
    DNS = 'DNS'
    HTTP = 'HTTP'
    SSL = 'SSL'
    NTP = 'NTP'
    ANCHORING = 'Anchoring'


class Setting(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'User Setting (' + str(self.id) + ') - username: ' + str(self.user.get_username())


class Notification(models.Model):
    # id = models.AutoField(primary_key=True)
    setting = models.ForeignKey(Setting, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=30)
    config = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Notification (' + str(self.setting.id) + ') - name: ' + str(self.name)


class Widget(models.Model):
    # id = models.AutoField(primary_key=True)
    setting = models.ForeignKey(Setting, null=False, blank=False, on_delete=models.CASCADE)
    type = models.CharField(null=False, blank=False, max_length=30)
    position = models.SmallIntegerField(null=False, blank=False)

    def __str__(self):
        return 'Widget (' + str(self.setting.id) + ') - type: ' + str(self.type)


class AutonomousSystem(models.Model):
    # id = models.AutoField(primary_key=True)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, null=False, blank=False)
    number = models.PositiveIntegerField(primary_key=True, null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=30)

    # measurement = models.ForeignKey(MeasurementCollection, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return 'Username (' + str(self.setting.user.get_username()) + ') ' + 'AS' + str(self.number) + ' - ' + self.name

    class Meta:
        verbose_name_plural = "Autonomous Systems"


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=30)

    def __str__(self):
        return 'Tag (' + str(self.id) + ') - ' + self.name


class MeasurementCollection(models.Model):
    id = models.AutoField(primary_key=True)
    autonomous_system = models.OneToOneField(AutonomousSystem, null=False, blank=False, on_delete=models.CASCADE)
    type = models.CharField(MeasurementType, choices=MeasurementType.choices, default=None, max_length=10,
                            null=False, blank=False)
    target = models.CharField(null=False, blank=False, max_length=30)
    tag = models.ManyToManyField(Tag, blank=False)

    def __str__(self):
        return 'MeasurementCollection (' + str(self.id) + ') - target: ' + self.target

    class Meta:
        verbose_name_plural = "Measurement Collections"


class Probe(models.Model):
    id = models.AutoField(primary_key=True)
    probe_id = models.PositiveIntegerField(null=False, blank=False)
    measurement = models.ForeignKey(MeasurementCollection, on_delete=models.CASCADE, null=False, blank=False)
    as_number = models.PositiveIntegerField(null=False, blank=False)
    location = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Probe (' + str(self.probe_id) + ') - location: ' + self.location


class MeasurementPoint(models.Model):
    id = models.AutoField(primary_key=True)
    probe = models.ForeignKey(Probe, on_delete=models.CASCADE, null=False, blank=False)
    time = models.DateTimeField(null=False, blank=False)
    round_trip_time_ms = models.PositiveIntegerField(null=False, blank=False)
    hops_total = models.PositiveSmallIntegerField(null=False, blank=False)

    def __str__(self):
        return 'Measurement Point (' + str(self.id) + ') - probe: ' + str(self.probe.probe_id)

    class Meta:
        verbose_name_plural = "Measurement Points"


class Hop(models.Model):
    # id = models.AutoField(primary_key=True)
    measurement_point = models.ForeignKey(MeasurementPoint, on_delete=models.CASCADE, null=False, blank=False)
    current_hop = models.PositiveSmallIntegerField(null=False, blank=False)
    round_trip_time_ms = models.PositiveIntegerField(null=False, blank=False)
    as_number = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return 'Hop (' + str(self.current_hop) + ') - Measurement Point: ' + str(self.measurement_point.id)


class DetectionMethod(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(null=False, blank=False, max_length=30)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return 'Detection Method (' + str(self.id) + ')'

    class Meta:
        verbose_name_plural = "Detection Methods"


class DetectionMethodSetting(models.Model):
    # id = models.AutoField(primary_key=True)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, null=False, blank=False)
    detection_method = models.ManyToManyField(DetectionMethod, blank=False)

    def __str__(self):
        return 'Detection Method Setting (' + str(self.setting.id) + ')' + \
               ' - username: ' + str(self.setting.user.get_username())

    class Meta:
        verbose_name_plural = "Detection Method Settings"


class Anomaly(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(null=False, blank=False)
    ip_address = models.CharField(null=False, blank=False, max_length=20)
    autonomous_system = models.ForeignKey(AutonomousSystem, on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    measurement_type = models.CharField(MeasurementType, choices=MeasurementType.choices, default=None, max_length=10,
                                        blank=False, null=False)
    detection_method = models.ForeignKey(DetectionMethod, on_delete=models.CASCADE, null=False, blank=False)
    medium_value = models.FloatField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    anomaly_score = models.FloatField(null=False, blank=False)
    prediction_value = models.BooleanField(null=False, blank=False)
    asn_error = models.PositiveIntegerField(null=True, blank=False)

    def __str__(self):
        return 'Anomaly (' + str(self.id) + ') -  ip: ' + self.ip_address + ' - ASN' + str(self.autonomous_system.number)

    class Meta:
        verbose_name_plural = "Anomalies"


class Feedback(models.Model):
    anomaly = models.OneToOneField(Anomaly, on_delete=models.CASCADE, null=False, blank=False)
    response = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return 'Feedback on anomaly(' + str(self.anomaly.id) + ')'

    class Meta:
        verbose_name_plural = "Feedback"

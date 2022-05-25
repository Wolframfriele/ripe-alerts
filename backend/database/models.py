# This class contains all entities which are later converted to tables by Django.
from enum import Enum
from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet


class MeasurementType(models.TextChoices):
    PING = 'ping'
    TRACEROUTE = 'traceroute'
    DNS = 'DNS'
    HTTP = 'HTTP'
    SSL = 'SSL'
    NTP = 'NTP'
    ANCHORING = 'anchoring'


class Setting(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'User Setting (' + str(self.id) + ') - username: ' + str(self.user.get_username())

    @staticmethod
    def get_user_settings(username: str):
        if not User.objects.filter(username=username).exists():
            return None
        user = User.objects.get(username=username)
        if not Setting.objects.filter(user=user).exists():
            Setting.objects.create(user=user)
        return Setting.objects.get(user=user)


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
    setting = models.OneToOneField(Setting, on_delete=models.CASCADE, null=False, blank=False, unique=True)
    number = models.PositiveIntegerField(null=False, blank=False)
    name = models.TextField(null=False, blank=False)

    # measurement = models.ForeignKey(MeasurementCollection, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.setting.user.get_username()) + ': ' + 'AS' + str(self.number) + ' - ' + self.name

    class Meta:
        verbose_name_plural = "Autonomous Systems"

    @staticmethod
    def register_asn(setting: Setting, system_number: int, location: str):
        autonomous_system_registered = AutonomousSystem.objects.filter(setting_id=setting.id).exists()
        if not autonomous_system_registered:
            AutonomousSystem.objects.create(setting=setting, number=system_number, name=location)
        elif autonomous_system_registered:
            autonomous_system = AutonomousSystem.objects.get(setting_id=setting.id)
            autonomous_system.number = system_number
            autonomous_system.name = location
            autonomous_system.save()
        return AutonomousSystem.objects.get(setting_id=setting.id)

    @staticmethod
    def get_asn_by_username(username: str):
        if not User.objects.filter(username=username).exists():
            return None
        user = User.objects.get(username=username)
        if not Setting.objects.filter(user=user).exists():
            return None
        setting = Setting.objects.get(user=user)
        if not AutonomousSystem.objects.filter(setting=setting).exists():
            return None
        system = AutonomousSystem.objects.get(setting=setting)
        return system


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, null=False, blank=False, max_length=30)

    def __str__(self):
        return 'Tag (' + str(self.id) + '): ' + self.name

    @staticmethod
    def get_tag_ids(tags: dict) -> list[int]:
        result: list[int] = []
        for tag in tags:
            if Tag.objects.filter(name=tag).exists():
                result.append(Tag.objects.get(name=tag).id)
            else:
                tag_i = Tag.objects.create(name=tag)
                tag_i.save()
                result.append(tag_i.id)
        return result


class MeasurementCollection(models.Model):
    id = models.AutoField(primary_key=True)
    autonomous_system = models.ForeignKey(AutonomousSystem, null=False, blank=False, on_delete=models.CASCADE)
    type = models.CharField(MeasurementType, choices=MeasurementType.choices, default=None, max_length=10,
                            null=False, blank=False)
    target = models.CharField(null=False, blank=False, max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    measurement_id = models.PositiveIntegerField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.description + ' (' + str(self.id) + ')'

    class Meta:
        verbose_name_plural = "Measurement Collections"

    @staticmethod
    def delete_all_by_asn(system: AutonomousSystem) -> None:
        system_exist = MeasurementCollection.objects.filter(autonomous_system=system).exists()
        if system_exist:
            collections = MeasurementCollection.objects.all().filter(autonomous_system=system)
            for x in collections:
                x.delete()


class Probe(models.Model):
    id = models.AutoField(primary_key=True)
    probe = models.PositiveIntegerField(null=False, blank=False)
    measurement = models.ForeignKey(MeasurementCollection, on_delete=models.CASCADE, null=False, blank=False)
    as_number = models.PositiveIntegerField(null=False, blank=False)
    country = models.TextField(null=False, blank=True)
    city = models.TextField(null=False, blank=True)

    def __str__(self):
        return 'Probe (' + str(self.probe) + ') - location: ' + self.city


class MeasurementPoint(models.Model):
    id = models.AutoField(primary_key=True)
    probe = models.ForeignKey(Probe, on_delete=models.CASCADE, null=False, blank=False)
    time = models.DateTimeField(null=False, blank=False)
    round_trip_time_ms = models.FloatField(null=True, blank=False)
    hops_total = models.PositiveSmallIntegerField(null=False, blank=False)

    def __str__(self):
        return 'Measurement Point (' + str(self.id) + ')'  # ' - probe: ' + str(self.probe.id)

    class Meta:
        verbose_name_plural = "Measurement Points"


class Hop(models.Model):
    # id = models.AutoField(primary_key=True)
    measurement_point = models.ForeignKey(MeasurementPoint, on_delete=models.CASCADE, null=False, blank=False)
    current_hop = models.PositiveSmallIntegerField(null=False, blank=False)
    round_trip_time_ms = models.PositiveIntegerField(null=True, blank=True)
    ip_address = models.CharField(null=True, blank=True, max_length=50)
    as_number = models.PositiveIntegerField(null=True, blank=False)

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
    ip_address = models.TextField(null=False, blank=False)
    autonomous_system = models.ForeignKey('AutonomousSystem', on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    measurement_type = models.CharField(MeasurementType, choices=MeasurementType.choices, default=None, max_length=10,
                                        blank=False, null=False)
    detection_method = models.ForeignKey(DetectionMethod, on_delete=models.CASCADE, null=False, blank=False)
    mean_increase = models.FloatField(null=False, blank=False)
    anomaly_score = models.FloatField(null=False, blank=False)
    prediction_value = models.BooleanField(null=False, blank=False)
    asn = models.PositiveIntegerField(null=True, blank=False)

    def __str__(self):
        return 'Anomaly (' + str(self.id) + ') -  ip: ' + self.ip_address + ' - ASN' + str(
            self.autonomous_system.number)

    class Meta:
        verbose_name_plural = "Anomalies"


class Feedback(models.Model):
    anomaly = models.OneToOneField(Anomaly, on_delete=models.CASCADE, null=False, blank=False)
    response = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return 'Feedback on anomaly (' + str(self.anomaly.id) + ')'

    class Meta:
        verbose_name_plural = "Feedback"

    @staticmethod
    def get_feedback(anomaly_id: int):
        feedback_exist = Feedback.objects.filter(anomaly_id=anomaly_id).exists()
        if feedback_exist:
            feedback = Feedback.objects.get(anomaly_id=anomaly_id)
            return feedback.response
        else:
            return None

    @staticmethod
    def create_or_update(anomaly_id: int, response: bool):
        feedback_exist = Feedback.objects.filter(anomaly_id=anomaly_id).exists()
        if feedback_exist:
            feedback = Feedback.objects.get(anomaly_id=anomaly_id)
            feedback.response = response
            feedback.save()
        elif not feedback_exist:
            feedback = Feedback.objects.create(anomaly_id=anomaly_id, response=response)
            feedback.save()

from django.db import models
from django.contrib.auth.models import User
from ripe_atlas.models import Measurement
import time

def current_unixtime():
    return int(time.time())

class ASN(models.Model):
    as_number = models.IntegerField(null=True)

class Anomaly(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.TimeField(null=True)
    ip_address = models.CharField(max_length=20, null=True)
    asn_settings_id = models.ForeignKey(ASN, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=1000, null=True)
    measurement_type = models.CharField(max_length=100, null=True)
    detection_method_id = models.IntegerField(null=True)
    medium_value = models.FloatField(null=True)
    value = models.FloatField(null=True)
    anomaly_score = models.FloatField(null=True)
    prediction_value = models.BooleanField(null=True)
    asn_error = models.IntegerField(null=True)
    

class Feedback(models.Model):
    anomaly_id = models.ForeignKey(Anomaly, on_delete=models.CASCADE)
    feedback = models.BooleanField(null=True)

# class AlertConfiguration(models.Model):
#     alert_configuration_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
#     alert_configuration_type = models.CharField(max_length=100)
#     alert_configuration = models.JSONField()

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['user', 'measurement', 'alert_configuration_type'],
#                                     name='unique_user_alert_configuration_on_measurement')
#         ]

# class Anomaly(models.Model):

#     anomaly_id = models.AutoField(primary_key=True)
#     alert_configuration = models.ForeignKey(AlertConfiguration, on_delete=models.CASCADE)
#     description = models.TextField()
#     label = models.BooleanField(null=True)
#     datetime = models.BigIntegerField(default=current_unixtime)
#     is_alert = models.BooleanField(default=False)

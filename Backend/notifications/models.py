from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class NotificationPlatform(models.Model):
    objects = None
    notification_platform_id = models.AutoField(primary_key=True)
    notification_platform_name = models.CharField(max_length=100)
    notification_platform_configuration = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

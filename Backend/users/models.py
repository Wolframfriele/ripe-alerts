from django.db import models
from django.contrib.auth.models import User


class RipeUser(models.Model):
    user = models.OneToOneField(User, related_name='ripe_user', on_delete=models.CASCADE)
    initial_setup_complete = models.BooleanField(default=False)
    ripe_api_token = models.UUIDField(null=True, blank=False)

    def __str__(self):
        return str(self.ripe_api_token)


class TimezoneConfiguration(models.Model):
    timezone_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='timezone_configuration', on_delete=models.CASCADE)
    timezone = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    usage = models.BooleanField()

    def __str__(self):
        return self.timezone

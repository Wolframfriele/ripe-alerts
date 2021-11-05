from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class RipeUser(models.Model):
    user = models.OneToOneField(User, related_name='ripe_api_token', on_delete=models.CASCADE)
    ripe_api_token = models.UUIDField(null=False, blank=False)

    def __str__(self):
        return str(self.ripe_api_token)
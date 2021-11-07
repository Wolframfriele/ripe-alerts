from django.contrib import admin
from .models import AlertConfiguration, Measurement, Alert

# Register your models here.


class AlertConfigurationInline(admin.TabularInline):
    model = AlertConfiguration




admin.site.register(AlertConfiguration)
admin.site.register(Alert)





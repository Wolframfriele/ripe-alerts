from django.contrib import admin
from .models import AlertConfiguration, Anomaly

# Register your models here.


class AnomalyInline(admin.TabularInline):
    model = Anomaly


class AlertConfigurationInline(admin.TabularInline):
    model = AlertConfiguration


class AlertConfigurationAdmin(admin.ModelAdmin):
    inlines = [AnomalyInline]


admin.site.register(AlertConfiguration, AlertConfigurationAdmin)
admin.site.register(Anomaly)





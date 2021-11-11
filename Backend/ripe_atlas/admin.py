from django.contrib import admin
from alert_configuration.admin import AlertConfigurationInline
from .models import Measurement, System

# Register your models here.


class MeasurementInline(admin.TabularInline):
    model = Measurement


class MeasurementAdmin(admin.ModelAdmin):
    inlines = [AlertConfigurationInline]


class SystemAdmin(admin.ModelAdmin):
    inlines = [MeasurementInline]


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(System, SystemAdmin)
from django.contrib import admin
from alert_configuration.admin import AlertConfigurationInline
from .models import Measurement, Target

# Register your models here.


class MeasurementInline(admin.TabularInline):
    model = Measurement


class MeasurementAdmin(admin.ModelAdmin):
    inlines = [AlertConfigurationInline]


class TargetAdmin(admin.ModelAdmin):
    inlines = [MeasurementInline]


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Target, TargetAdmin)
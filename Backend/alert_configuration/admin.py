from django.contrib import admin
from .models import AlertConfiguration, Measurement, Target, Alert

# Register your models here.


class AlertConfigurationInline(admin.TabularInline):
    model = AlertConfiguration


class MeasurementInline(admin.TabularInline):
    model = Measurement


class TargetAdmin(admin.ModelAdmin):
    inlines = [MeasurementInline]


class MeasurementAdmin(admin.ModelAdmin):
    inlines = [AlertConfigurationInline]


admin.site.register(AlertConfiguration)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(Alert)





from django.contrib import admin
from .models import Measurement, Anchor
from notifications.models import NotificationPlatform

# Register your models here.


class MeasurementInline(admin.TabularInline):
    model = Measurement


class SystemAdmin(admin.ModelAdmin):
    inlines = [MeasurementInline]


admin.site.register(Measurement)
admin.site.register(Anchor, SystemAdmin)
admin.site.register(NotificationPlatform)

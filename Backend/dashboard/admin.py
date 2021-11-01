from django.contrib import admin
from django.db import models

from .models import AlertConfiguration, Measurement, Probe, RipeUser
from django.contrib.auth.models import User 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class RipeUserInline(admin.TabularInline):
    model = RipeUser
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [RipeUserInline]

class AlertConfigurationInline(admin.TabularInline):
    model = AlertConfiguration


class MeasurementInline(admin.TabularInline):
    model = Measurement


class ProbeAdmin(admin.ModelAdmin):
    inlines = [MeasurementInline]


class MeasurementAdmin(admin.ModelAdmin):
    inlines = [AlertConfigurationInline]

admin.site.register(AlertConfiguration)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Probe, ProbeAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
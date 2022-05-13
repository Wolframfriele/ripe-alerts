from django.contrib import admin
from .models import Anomaly, Feedback, ASN

# Register your models here.


class AnomalyInline(admin.TabularInline):
   model = Anomaly


# class AlertConfigurationInline(admin.TabularInline):
#     model = AlertConfiguration


# class AlertConfigurationAdmin(admin.ModelAdmin):
#     inlines = [AnomalyInline]


admin.site.register(Anomaly)
admin.site.register(Feedback)
admin.site.register(ASN)





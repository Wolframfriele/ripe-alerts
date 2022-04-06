from django.contrib import admin

from database.models import *

# Add Models to Django administration panel
admin.site.register(Setting)
admin.site.register(Notification)
admin.site.register(Widget)
admin.site.register(MeasurementCollection)
admin.site.register(AutonomousSystem)
admin.site.register(Probe)
admin.site.register(MeasurementPoint)
admin.site.register(Hop)
admin.site.register(DetectionMethodSetting)
admin.site.register(DetectionMethod)
admin.site.register(Anomaly)
admin.site.register(Feedback)
admin.site.register(Tag)

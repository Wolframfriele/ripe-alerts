from django.urls import path, include
from .apis import CreateMonitor, Feedback, MonitorProcess, Measurement

urlpatterns = [
    # path('', CreateMonitor.as_view()),
    path('', MonitorProcess.as_view()),
    path('feedback', Feedback.as_view()),
    path('measurement', Measurement.as_view())
]

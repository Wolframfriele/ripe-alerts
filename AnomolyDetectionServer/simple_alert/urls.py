from django.urls import path, include
from .apis import Feedback, MonitorProcess

urlpatterns = [
    # path('', CreateMonitor.as_view()),
    path('', MonitorProcess.as_view()),
    path('feedback', Feedback.as_view()),
]

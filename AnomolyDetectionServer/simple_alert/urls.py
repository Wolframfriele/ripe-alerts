from django.urls import path, include
from .apis import CreateMonitor, Feedback

urlpatterns = [
    path('', CreateMonitor.as_view()),
    path('feedback', Feedback.as_view())
]

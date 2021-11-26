from django.urls import path, include
from .apis import CreateMonitor

urlpatterns = [
    path('', CreateMonitor.as_view())
]

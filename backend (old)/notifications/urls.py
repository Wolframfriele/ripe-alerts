from django.urls import path
from .apis import PluginConfigSystem, AlertSystem

urlpatterns = [
    path('config', PluginConfigSystem.as_view(), name="atlas-notification-config"),
    path('publish', AlertSystem.as_view(), name="atlas-notification-broadcast")
]

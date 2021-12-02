from os import name
from django.urls import path
from .apis import  AlertConfigurationList, AlertList, LabelAlert

urlpatterns = [
    path('alert_configuration', AlertConfigurationList.as_view(), name='listcreate'),
    path('get_alerts', AlertList.as_view()),
    path('label_alert', LabelAlert.as_view())
]

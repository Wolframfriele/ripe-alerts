from django.urls import path
from .apis import AlertList, LabelAlert

urlpatterns = [
    path('get_alerts', AlertList.as_view()),
    path('label_alert', LabelAlert.as_view(), name="label-alert")
]

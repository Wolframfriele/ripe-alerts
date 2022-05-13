from django.urls import path
from .apis import AlertList, LabelAlert, FeedBack

urlpatterns = [
    path('get_alerts', AlertList.as_view()),
    path('label_alert', LabelAlert.as_view(), name="label-alert"),
    path('feedback', FeedBack.as_view())
]

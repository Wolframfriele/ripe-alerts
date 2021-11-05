from os import name
from django.urls import path
from .views import AlertConfigurationDetail, AlertConfigurationList

urlpatterns = [
    path('alert_configuration/ <int:pk>/', AlertConfigurationDetail.as_view(), name="detailcreate"),
    path('alert_configuration', AlertConfigurationList.as_view(), name='listcreate'),
]

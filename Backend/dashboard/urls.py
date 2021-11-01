from os import name
from django.urls import path
from .views import AlertConfigurationDetail, AlertConfigurationList, UserDetail, RegistrationService

urlpatterns = [
    path('alert_configuration/ <int:pk>/', AlertConfigurationDetail.as_view(), name="detailcreate"),
    path('alert_configuration', AlertConfigurationList.as_view(), name='listcreate'),
    path('user', UserDetail.as_view(), name='userdetail'),
    path('registration-service', RegistrationService.as_view(), name="registration-service" )

]
from os import name
from django.urls import path
from .views import AlertConfigurationDetail, AlertConfigurationList, UserDetail, RegistrationService, MyAtlasProbes, \
    AtlasSearchProbes, RelevantMeasurements

urlpatterns = [
    path('alert_configuration/ <int:pk>/', AlertConfigurationDetail.as_view(), name="detailcreate"),
    path('alert_configuration', AlertConfigurationList.as_view(), name='listcreate'),
    path('user', UserDetail.as_view(), name='userdetail'),
    path('registration-service', RegistrationService.as_view(), name="registration-service"),
    path('atlas/my-probes', MyAtlasProbes.as_view(), name="atlas-probes"),
    path('atlas/probes', AtlasSearchProbes.as_view(), name="atlas-search-probes"),
    path('atlas/measurements', RelevantMeasurements.as_view(), name='atlas-relevant-measurements'),
]

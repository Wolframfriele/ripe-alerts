from django.urls import path
from .apis import UserDetail, RegistrationService, InitialSetup, ASNList

urlpatterns = [
    path('', UserDetail.as_view(), name='userdetail'),
    path('registration-service', RegistrationService.as_view(), name="registration-service"),
    path('initial-setup', InitialSetup.as_view(), name="initial-setup"),
    path('monitored-asns', ASNList.as_view())
]
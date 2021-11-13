from django.urls import path
from .apis import UserDetail, RegistrationService, InitialSetup

urlpatterns = [
    path('', UserDetail.as_view(), name='userdetail'),
    path('registration-service', RegistrationService.as_view(), name="registration-service"),
    path('initial-setup', InitialSetup.as_view())
]
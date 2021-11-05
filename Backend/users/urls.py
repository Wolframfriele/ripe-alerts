from django.urls import path
from .views import UserDetail, RegistrationService

urlpatterns = [
    path('', UserDetail.as_view(), name='userdetail'),
    path('registration-service', RegistrationService.as_view(), name="registration-service")
]
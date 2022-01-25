from django.urls import path
from .apis import AsnHost

urlpatterns = [
    path('asn', AsnHost.as_view(), name="asn-holder")
]

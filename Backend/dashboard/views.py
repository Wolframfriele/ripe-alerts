from django.db.models import query
from rest_framework import generics, request
from dashboard.models import AlertConfiguration
from django.core.exceptions import ObjectDoesNotExist
from.serializers import AlertConfigurationSerializer

# Create your views here.

class AlertConfigurationList(generics.ListCreateAPIView):
    # queryset = AlertConfiguration.objects.all()
    # print("test")
    serializer_class = AlertConfigurationSerializer
    def get_queryset(self):
        user = self.request.user
        try:
            print(user.ripeuser.ripe_api_token)
        except ObjectDoesNotExist:
            print("has no ripe token")
        print('test')
        return AlertConfiguration.objects.all()


class AlertConfigurationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlertConfiguration.objects.all()
    serializer_class = AlertConfigurationSerializer
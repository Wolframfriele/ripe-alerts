from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AlertConfiguration
from django.core.exceptions import ObjectDoesNotExist


class AlertConfigurationList(APIView):
    """List of alert configurations"""

    def get(self, request):
        """ get all AlertConfigurations belonging to user"""
        user = request.user
        try:
            print(user.ripe_api_token.ripe_api_token)
        except ObjectDoesNotExist:
            print("has no ripe token")

        return AlertConfiguration.objects.all()

    def post(self, request):
        """ Add new alert configurations"""

        return Response(data=None, status=status.HTTP_201_CREATED)


class AlertConfigurationDetail(APIView):
    def get(self):
        """ get specific AlertConfiguration """

    def put(self, request):
        """ Update alert configuration """


class AlertingSchemas(APIView):
    def get(self, request):
        """returns the configuration setting that are necessary for the type of alerts"""
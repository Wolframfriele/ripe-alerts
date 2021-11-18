
"""
Ripe ATLAS API interaction
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .interfaces import RipeInterface
from django.contrib.auth.models import User


class MyAtlasSystems(APIView):
    """
    Get all anchors and target of the user
    """

    def get(self, request):
        user_token = User.objects.get(id=2).ripe_user.ripe_api_token
        # user_token = request.user.ripe_user.ripe_api_token
        ripe_user_data = RipeInterface(user_token)
        return Response(ripe_user_data.get_my_anchors_targets())


class AtlasSearchSystems(APIView):
    """
    Search for targets and anchors in ripe atlas: the input could be one of these: asn, probe_id,host, ip_adres
    """

    def get(self, request):

        user_token = User.objects.get(id=2).ripe_user.ripe_api_token
        # user_token = request.user.ripe_user.ripe_api_token
        ripe_user_data = RipeInterface(user_token)
        filter_option: str = request.query_params.get('filter')
        if filter_option not in ['asn', 'host', 'ip_address', 'probe_id']:
            return Response({"error": "Invalid filter"}, status=status.HTTP_400_BAD_REQUEST)

        search_value: str = request.query_params.get('search_value')
        if search_value is None:
            return Response({"error": "search_value field is missing or null"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ripe_user_data.search_systems(filter_option, search_value), status=status.HTTP_200_OK)

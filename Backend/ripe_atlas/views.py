
"""
Ripe ATLAS API interaction
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .ripe_api import RipeUserData


class MyAtlasSystems(APIView):
    """
    Get all anchors and target of the user
    """

    def get(self, request):
        ripe_user_data = RipeUserData(request.user.ripe_user.ripe_api_token)
        return Response(ripe_user_data.get_owned_anchors_targets())


def identify_filter_type(search_value):

    return "ip_address"

    if ":" in search_value or "." in search_value:
        return "asn"
    if "mm":
        return "asn"
    if "host":
        return "host"
    if "probe_id":
        return "probe_id"
    raise ValueError


class AtlasSearchSystems(APIView):
    """
    Search for targets and anchors in ripe atlas: the input could be one of these: asn, probe_id,host, ip_adres
    """

    def get(self, request):

        ripe_user_data = RipeUserData(request.user.ripe_user.ripe_api_token)
        search_value: str = request.query_params.get('search_value')
        if search_value is None:
            return Response({"error": "search_value field is missing or null"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            filter_type = identify_filter_type(search_value)
            return Response(ripe_user_data.search_systems(filter_type, search_value), status.HTTP_200_OK)
        except ValueError:
            return Response({"error": f"invalid value"}, status.HTTP_400_BAD_REQUEST)
        return Response(result, status.HTTP_200_OK)


"""
Ripe ATLAS API interaction
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .interfaces import RipeInterface


class AsnHost(APIView):
    """Return holder of the ASN"""

    def get(self, request):
        asn = request.query_params.get("asn")
        if asn:
            return Response(RipeInterface.get_asn_host(asn), status=status.HTTP_200_OK)
        else:
            return Response({"error": "asn is required"}, status=status.HTTP_400_BAD_REQUEST)

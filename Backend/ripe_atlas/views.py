
"""
Ripe ATLAS API interaction
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .ripe_api import RipeUserData


class MyAtlasProbes(APIView):
    """
    Get all probes and anchors owned by the user from Ripe Atlas with relevant measurments
    """

    def get(self, request):
        ripe_user_data = RipeUserData(request.user.ripe_user.ripe_api_token)
        return Response(ripe_user_data.get_owned_anchors_probes())


class AtlasSearchProbes(APIView):
    """
    Search for probes in ripe atlas, search can be done on the following fields: "ASN", "Probe_id", "host" "prefix"
    """
    valid_filters = ['asn', 'probe_id', 'host', 'prefix']

    def get(self, request):

        ripe_user_data = RipeUserData(request.user.ripe_user.ripe_api_token)
        filter: str = request.query_params.get('filter')
        value: str = request.query_params.get('value', '')

        if filter not in AtlasSearchProbes.valid_filters:
            return Response({"error": "invalid filter, you can filter on asn, probe_id, prefix or host"},
                            status.HTTP_400_BAD_REQUEST)
        if filter == "probe_id" and value.isnumeric() is False:
            return Response({"error": "invalid probe_id"}, status.HTTP_400_BAD_REQUEST)

        try:
            probes = ripe_user_data.search_probes(filter, value)
            result = {filter: value}
            result.update(probes)
        except ValueError:
            return Response({"error": f"invalid {filter}"}, status.HTTP_400_BAD_REQUEST)
        return Response(result, status.HTTP_200_OK)


class RelevantMeasurements(APIView):
    """
    Returns relevant measurements belonging to a probe.
    Relevant measurements are anchoring measurements and user defined measurements targeting the probe.
    """

    def is_relevant_measurement_input_valid(self, relevant_measurement_input) -> tuple:
        is_anchor = relevant_measurement_input.get("is_anchor")
        address_v4 = relevant_measurement_input.get("address_v4")
        address_v6 = relevant_measurement_input.get("address_v6")
        if is_anchor is None:
            return False, Response({"error": "we need the is_anchor field"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(is_anchor, bool):
            return False, Response({"error": "is_anchor needs to be boolean"}, status=status.HTTP_400_BAD_REQUEST)
        if not address_v6 and not address_v4:
            return False, Response({"error": "we need at least an address_v4 or address_v6 field"},
                                   status=status.HTTP_400_BAD_REQUEST)
        return True,

    def get(self, request):
        valid, error_response = self.is_relevant_measurement_input_valid(request.data)
        if valid:
            ripe_user_data = RipeUserData(request.user.ripe_user.ripe_api_token)
            relevant_measurements = ripe_user_data.get_alertable_measurements_probe(request.data)
            return Response(relevant_measurements, status=status.HTTP_200_OK)
        else:
            return error_response

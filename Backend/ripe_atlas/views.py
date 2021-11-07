
"""
Ripe ATLAS API interaction
"""

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .ripe_api import get_anchors_probes_with_token, search_probes, get_relevant_measurements
from .serializers import TargetSerializer


class MyAtlasProbes(APIView):
    """
    Get all probes and anchors owned by the user from Ripe Atlas with relevant measurments
    """

    def get(self, request):
        return Response(get_anchors_probes_with_token(request.user.ripe_api_token))


class AtlasSearchProbes(APIView):
    """
    Search for probes in ripe atlas, search can be done on the following fields: "ASN", "Probe_id", "host" "prefix"
    """
    valid_filters = ['asn', 'probe_id', 'host', 'prefix']

    def get(self, request):

        filter: str = request.query_params.get('filter')
        value: str = request.query_params.get('value', '')
        if filter not in AtlasSearchProbes.valid_filters:
            return Response({"error": "invalid filter, you can filter on asn, probe_id, prefix or host"},
                            status.HTTP_400_BAD_REQUEST)
        if filter == "probe_id" and value.isnumeric() is False:
            return Response({"error": "invalid probe_id"}, status.HTTP_400_BAD_REQUEST)
        try:
            probes = search_probes(request.user.ripe_user.ripe_api_token, filter, value)
            result = {filter: value}
            result.update(probes)
        except ValueError:
            return Response({"error": f"invalid {filter}"}, status.HTTP_400_BAD_REQUEST)
        return Response(result, status.HTTP_200_OK)


class RelevantMeasurements(APIView):
    """
    Returns relevant measurements belonging to the given probes.
    Relevant measurements are anchoring measurements and user defined measurements targeting the probe.
    (Geen MVP) ook measurement waarvan de probe source is van de meting
    """

    def get(self, request):
        serialized_probes = TargetSerializer(data=request.data, many=True)
        token = request.user.ripe_user.ripe_api_token
        if serialized_probes.is_valid():
            measurements = []
            for probe in serialized_probes.validated_data:
                ip_v4 = probe.get('ip_v4')
                ip_v6 = probe.get('ip_v6')
                ip = probe.get('ip')
                host = probe.get('host')
                asn = probe.get('asn')

                if ip_v4:
                    result = {
                        "ip_v4": ip_v4,
                    }
                    result.update(get_relevant_measurements(token, ip=ip_v4))
                    measurements.append(result)
                if ip_v6:
                    result = {
                        "ip_v6": ip_v6,
                    }
                    result.update(get_relevant_measurements(token, ip=ip_v6))
                    measurements.append(result)
                if host:
                    result = {
                        "host": host,
                    }
                    result.update(get_relevant_measurements(token, host=host))
                    measurements.append(result)
                if ip:
                    result = {
                        "ip": ip,
                    }
                    result.update(get_relevant_measurements(token, ip=ip))
                    measurements.append(result)
                if asn:
                    result = {
                        "asn": ip,
                    }
                    result.update(get_relevant_measurements(token, asn=asn))
                    measurements.append(result)
            return Response(measurements, status=status.HTTP_200_OK)
        else:
            return Response(serialized_probes.errors, status=status.HTTP_400_BAD_REQUEST)
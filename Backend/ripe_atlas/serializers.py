from rest_framework import serializers
from .models import Measurement, Target


class TargetSerializer(serializers.Serializer):
    prefix_v4 = serializers.CharField(required=False, allow_null=True)
    prefix_v6 = serializers.CharField(required=False, allow_null=True)
    ip_v4 = serializers.CharField(required=False, allow_null=True)
    ip_v6 = serializers.CharField(required=False, allow_null=True)
    ip = serializers.CharField(required=False, allow_null=True)
    host = serializers.CharField(required=False, allow_null=True)
    asn = serializers.CharField(required=False, allow_null=True)
    probe_id = serializers.CharField(required=False)
    location = serializers.ListField(required=False)

    def validate(self, data):
        """
        Validate data
        """

        #check if we have ip.
        if not data.get('ip_v4') and not data.get('ip_v6') and not data.get('ip') and not data.get('host') \
                and not data.get('asn'):
            raise serializers.ValidationError("we need at least input for ip_v4, ip_v6, ip, host or asn")
        return data


# class ProbeSerializer(serializers.Serializer):
#
#     prefix_v4 = serializers.CharField(required=False, allow_null=True)
#     prefix_v6 = serializers.CharField(required=False, allow_null=True)
#     ip_v4 = serializers.CharField(required=False, allow_null=True)
#     ip_v6 = serializers.CharField(required=False, allow_null=True)
#     ip = serializers.CharField(required=False, allow_null=True)
#     host = serializers.CharField(required=False, allow_null=True)
#     asn_v4 = serializers.CharField(required=False, allow_null=True)
#     asn_v6 = serializers.CharField(required=False, allow_null=True)
#     probe_id = serializers.CharField(required=False)
#     location = serializers.ListField(required=False)
#
#     def validate(self, data):
#         """
#         Validate data
#         """
#         #check if we have ip.
#         if not data.get('ip_v4') and not data.get('ip_v6') and not data.get('ip') and not data.get('host') \
#                 and not data.get('asn'):
#             raise serializers.ValidationError("we need at least input for ip_v4, ip_v6, ip, host or asn")
#         return data

class ProbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        exclude = ['target_id']
        extra_kwargs = {
            'probe_id': {
                'validators': [],
            }
        }

    def validate(self, data):
        """
        Validate data
        """
        # check if we have ip.
        if not data.get('address_v4') and not data.get('prefix_v4') and not data.get('address_v6') \
                and not data.get('prefix_v6') and not data.get('host') \
                and not data.get('asn_v4') and not data.get('asn_v6'):
            raise serializers.ValidationError("we need at least probe information for one the following fields: address_v4, "
                                              "address_v6, host asn, prefix_v4 or prefix_v6")
        return data


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ["measurement_id", "type"]
        extra_kwargs = {
            'measurement_id': {
                'validators': [],
            }
        }

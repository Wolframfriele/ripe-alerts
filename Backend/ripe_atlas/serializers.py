from rest_framework import serializers
from .models import Measurement, System


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
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
        fields = ["measurement_id", "description", "type", "interval"]
        extra_kwargs = {
            'measurement_id': {
                'validators': [],
            }
        }


TARGET_REQUIRED_FIELDS = ['target_ip', 'target_address', 'target_asn', 'target', 'measurements']
ANCHOR_REQUIRED_FIELDS = ['address_v4', 'address_v6', 'prefix_v4', 'prefix_v6', 'asn_v4', 'asn_v6', 'host']


class TargetSerializer(serializers.Serializer):
    measurements = MeasurementSerializer(many=True)
    target_ip = serializers.CharField(max_length=100, required=True)
    target_asn = serializers.CharField(max_length=10, required=True, allow_null=True)
    target_prefix = serializers.CharField(max_length=100, required=True, allow_null=True)
    target = serializers.CharField(max_length=100, required=True, allow_null=True)

    def validate_measurements(self, measurements):
        if len(measurements) < 1:
            raise serializers.ValidationError("We need at least 1 measurement")
        return measurements


class AnchorSerializer(serializers.ModelSerializer):
    anchor_measurements = MeasurementSerializer(many=True)

    class Meta:
        model = System
        exclude = ['system_id']
        extra_kwargs = {
            'probe_id': {
                'validators': [],
            }
        }

    def validate_measurements(self, measurements):
        if len(measurements) < 1:
            raise serializers.ValidationError("We need at least 1 measurement")
        return measurements

    def validate(self, anchor):
        if not anchor.get('address_v4') and not anchor.get('prefix_v4') and not anchor.get('address_v6') \
                and not anchor.get('prefix_v6') and not anchor.get('host') \
                and not anchor.get('asn_v4') and not anchor.get('asn_v6'):
            raise serializers.ValidationError(
                {"error": "we need at least anchor information of one of the following fields: "
                          "address_v4, address_v6, host asn, prefix_v4 or prefix_v6"})
        return anchor


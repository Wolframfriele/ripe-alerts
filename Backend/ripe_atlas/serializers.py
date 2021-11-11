from rest_framework import serializers
from .models import Measurement, System


class ProbeSerializer(serializers.ModelSerializer):
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
        fields = ["measurement_id", "type"]
        extra_kwargs = {
            'measurement_id': {
                'validators': [],
            }
        }

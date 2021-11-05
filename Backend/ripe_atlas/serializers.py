from rest_framework import serializers


class TargetSerializer(serializers.Serializer):
    prefix_v4 = serializers.CharField(required=False)
    prefix_v6 = serializers.CharField(required=False)
    ip_v4 = serializers.CharField(required=False)
    ip_v6 = serializers.CharField(required=False)
    ip = serializers.CharField(required=False)
    host = serializers.CharField(required=False)
    asn = serializers.CharField(required=False)
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
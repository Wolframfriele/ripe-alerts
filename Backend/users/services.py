from ripe_atlas.models import Measurement, Asn, Anchor
from alert_configuration.models import AlertConfiguration
from .models import RipeUser
from ripe_atlas.interfaces import RipeInterface


def store_measurements(measurements, system, user):
    for measurement in measurements:
        measurement = Measurement.objects.get_or_create(**measurement, system=system)[0]
        print(f"storing alert configuration for measurement: {measurement.measurement_id} ")
        alert_config = {"max_packet_loss": 75}
        AlertConfiguration.objects.get_or_create(user=user,
                                                 measurement=measurement,
                                                 alert_configuration_type=measurement.type,
                                                 alert_configuration=alert_config)


def transform_target(target):
    target['host'] = target.pop('target')
    if '.' in target['target_ip']:
        target['address_v4'] = target.pop('target_ip')
        target['asn_v4'] = target.pop('target_asn')
        target['prefix_v4'] = target.pop('target_prefix')
    else:
        target['address_v6'] = target.pop('target_ip')
        target['asn_v6'] = target.pop('target_asn')
        target['prefix_v6'] = target.pop('target_prefix')
    return target


class InitialSetupService:


    @staticmethod
    def store_initial_setup(validated_data):
        # store targets, anchors, measurements and related alert_configuration in database

        for asn, anchors in validated_data['anchors_by_asn'].items():
            asn = Asn.objects.get_or_create(asn=asn)[0]
            for anchor in anchors:
                # store anchor
                anchor: Anchor = Anchor.objects.get_or_create(anchor_id=anchor['id'], ip_v4=anchor['ip_v4'],
                                                      ip_v6=anchor['ip_v6'], asn=asn, fqdn=anchor['fqdn'])[0]
                # collect anchoring meaurements ping and traceroute
                measurements = []
                if anchor.ip_v4:
                    measurements.extend(RipeInterface.get_anchoring_measurements(target_address=anchor.ip_v4))
                if anchor.ip_v6:
                    measurements.extend(RipeInterface.get_anchoring_measurements(target_address=anchor.ip_v6))
                # store anchors and related measurements to the database
                for measurement in measurements:
                    measurement = Measurement(measurement_id=measurement['id'], type=measurement['type'],
                                              description=measurement['description'], interval=measurement["interval"],
                                              anchor=anchor)
                    measurement.save()

            # tell the ai server to create an alert configuration for the user based on the asn

        # store the email
        print("storing the email")

        return True

        # # set initial_setup_complete to true.
        # ripe_user = RipeUser.objects.filter(user=validated_data['user'])
        # ripe_user.update(initial_setup_complete=True)

        # return {"username": validated_data['user'].username,
        #         "ripe_api_token": validated_data['user'].ripe_user.ripe_api_token,
        #         "initial_setup_complete": True}
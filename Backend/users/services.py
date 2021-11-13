from ripe_atlas.models import Measurement, System
from alert_configuration.models import AlertConfiguration
from .models import RipeUser


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
        for target in validated_data['targets']:
            # store target related measurements and make an alert configuration based on the measurement.
            target = transform_target(target)
            target['target_type'] = 'target'
            measurements = target.pop('measurements')
            system = System.objects.get_or_create(**target)[0]
            store_measurements(measurements, system, validated_data['user'])

        for anchor in validated_data['anchors']:
            measurements = anchor.pop('measurements')
            system = System.objects.get_or_create(**anchor)[0]
            store_measurements(measurements, system, validated_data['user'])

        # store the email
        print("storing the email")

        # set initial_setup_complete to true.
        ripe_user = RipeUser.objects.filter(user=validated_data['user'])
        ripe_user.update(initial_setup_complete=True)

        return {"username": validated_data['user'].username,
                "ripe_api_token": validated_data['user'].ripe_user.ripe_api_token,
                "initial_setup_complete": True}
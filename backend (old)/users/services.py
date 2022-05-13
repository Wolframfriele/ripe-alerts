from ripe_atlas.models import Measurement, Asn, Anchor
from django.db import IntegrityError
#from alert_configuration.models import AlertConfiguration
from .models import RipeUser
from ripe_atlas.interfaces import RipeInterface
import requests

AI_SERVER_MONITOR_URL = "http://ai-server:8001/monitor/"


class InitialSetupService:

    @staticmethod
    def store_initial_setup(validated_data):
        """store targets, anchors, measurements and related alert_configuration in database, if succeeded we send a
        signal to thje ai-server to start monitoring the asns"""

        for asn, anchors in validated_data['anchors_by_asn'].items():
            asn = Asn.objects.get_or_create(asn=asn)[0]
            for anchor in anchors:
                # store anchor
                anchor: Anchor = Anchor.objects.get_or_create(anchor_id=anchor['id'], ip_v4=anchor['ip_v4'],
                                                              ip_v6=anchor['ip_v6'], asn=asn, fqdn=anchor['fqdn'])[0]
                # collect anchoring measurements ping and traceroute
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
                    #try:
                    #    AlertConfiguration(user=validated_data['user'], measurement=measurement,
                    #                       alert_configuration_type="default", alert_configuration=
                    #                       {"default": "wordt later geimplementeerd"}).save()
                    #except IntegrityError:
                    #    continue

            # Send signal to ai server to start monitoring the asns
            requests.post(url=AI_SERVER_MONITOR_URL, json={"asns": validated_data['asns']})


        # store the email
        print("storing the email")


        # set initial_setup_complete to true.

        ripe_user = RipeUser.objects.filter(user=validated_data['user'])
        if len(ripe_user) == 0:
            RipeUser.objects.create(user=validated_data['user'], initial_setup_complete=True)
        else:
            ripe_user.update(initial_setup_complete=True)

        return {"username": validated_data['user'].username,
                "ripe_api_token": validated_data['user'].ripe_user.ripe_api_token,
                "initial_setup_complete": True}


def get_monitored_asns(user_id: int):
    return Asn.objects.raw(
        """SELECT DISTINCT asn
            FROM  ripe_atlas_asn as a
            JOIN ripe_atlas_anchor as b ON b.asn_id = a.asn
            JOIN ripe_atlas_measurement as c ON c.anchor_id = b.anchor_id 
            JOIN alert_configuration_alertconfiguration as d ON d.measurement_id = c.measurement_id
            WHERE d.user_id = %s
        """, [user_id])

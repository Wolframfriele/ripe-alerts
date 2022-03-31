import json

import requests
import constants
from collections import defaultdict

from ripe_interface.anchor import Anchor


class RipeRequests:

    @staticmethod
    def get_anchors(as_number: int) -> list[Anchor]:
        """Returns all Anchors based on the autonomous system number, if empty then there have been no anchors found."""
        params = {"as_v4": str(as_number)}
        response = requests.get(url=constants.ANCHORS_URL, params=params).json()
        results = response.get('results')
        if not results:
            return []
        else:
            anchor_array = []
            for x in results:
                anchor = Anchor(**x)
                anchor_array.append(anchor)
        return anchor_array

    @staticmethod
    def get_anchoring_measurements(target_address: str) -> list:
        """Returns a list of anchoring measurements in the same form as specified by ripe atlas documentation, the
        type of measurements that are returned are supported by the monitoring system
        Keyword arguments:
        target_address: str, can be ip_v4 or ip_v6
        """
        params = {
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_ip': target_address,
            'fields': constants.WANTED_ANCHOR_MEASUREMENT_FIELDS
        }
        response = requests.get(constants.MEASUREMENTS_URL, params=params).json()
        return [measurement for measurement in response['results'] if
                measurement['type'] in constants.SUPPORTED_TYPE_MEASUREMENTS]

    @staticmethod
    def get_asn_host(asn: int):
        response = requests.get(constants.RIPE_STATS_ASN, params={"resource": asn}).json()
        return {"holder": response['data'].get('holder')}

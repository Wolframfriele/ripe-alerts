import requests

from ripe_interface.anchor import AnchoringMeasurement, Anchor

# from .anchor import Anchor
# "RIPE API URLS"

RIPE_BASE_URL = "https://atlas.ripe.net/api/v2/"
MEASUREMENTS_URL = RIPE_BASE_URL + "measurements/"
MY_MEASUREMENTS_URL = MEASUREMENTS_URL + "my/"
CURRENT_PROBES_URL = RIPE_BASE_URL + "credits/income-items/"
ANCHORS_URL = RIPE_BASE_URL + "anchors/"
PROBES_URL = RIPE_BASE_URL + "probes/"
RIPE_STATS_ASN_NEIGHBOURS = "https://stat.ripe.net/data/asn-neighbours/data.json"
RIPE_STATS_ASN = "https://stat.ripe.net/data/as-overview/data.json"

# """RIPE RESPONSE FIELDS"""

WANTED_PROBE_FIELDS = "id,is_anchor,type,address_v4,address_v6,asn_v4,asn_v6,geometry,prefix_v4,prefix_v6,description"
WANTED_ANCHOR_FIELDS = "id,ip_v4,ipv6,as_v4,as_v6,geometry,prefix_v4,prefix_v6,fqdn"
WANTED_ANCHOR_MEASUREMENT_FIELDS = "id,type,interval,description,tags,target"
WANTED_MEASUREMENT_FIELDS = "id,type,interval,description,target_ip,target,target_asn,target_prefix"


class RipeRequests:

    @staticmethod
    def get_anchors(as_number: int) -> list[Anchor]:
        """Returns all anchors based on the autonomous system number, if empty then there have been no anchors found.
           Disclaimer: Not all autonomous systems contain anchors, some contain probes only."""
        params = {"as_v4": str(as_number)}
        response = requests.get(url=ANCHORS_URL, params=params).json()
        results = response.get('results')  # There are multiple anchors.
        if not results:
            return []
        else:
            anchor_array = []
            for x in results:
                anchor = Anchor(**x)
                anchor_array.append(anchor)
        return anchor_array

    @staticmethod
    def autonomous_system_exist(as_number: int) -> bool:
        """Returns whether the autonomous system number exists or not. """
        params = {"asn_v4": str(as_number)}
        response = requests.get(url=PROBES_URL, params=params).json()
        probes_amount = response.get('count')
        return not probes_amount == 0

    @staticmethod
    def get_anchoring_measurements(target_address: str) -> list[AnchoringMeasurement]:
        """Returns a list of anchoring measurements in the same form as specified by ripe atlas documentation, the
        type of measurements that are returned are supported by the monitoring system
        Keyword arguments:
        target_address: str, can be ip_v4 or ip_v6
        """
        params = {
            'tags': 'anchoring',
            'status': 'ongoing',
            'target_ip': target_address,
            'fields': WANTED_ANCHOR_MEASUREMENT_FIELDS
        }
        response = requests.get(MEASUREMENTS_URL, params=params).json()
        results = response.get('results')
        measurements = []
        for x in results:
            anchor_measurement = AnchoringMeasurement(**x)
            measurements.append(anchor_measurement)
        return measurements

    @staticmethod
    def get_company_name(as_number: int) -> str:
        """ Returns the company name of an autonomous system. """
        company: str = ""
        params = {"resource": str(as_number)}
        response = requests.get(url=RIPE_STATS_ASN, params=params).json()
        results = response.get('data')
        if results['holder']:
            company = results['holder']
        return company

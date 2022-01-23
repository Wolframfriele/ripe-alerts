import requests
from collections import defaultdict

"""RIPE API URLS"""
RIPE_BASE_URL = "https://atlas.ripe.net/api/v2/"
MEASUREMENTS_URL = RIPE_BASE_URL + "measurements/"
MY_MEASUREMENTS_URL = MEASUREMENTS_URL + "my/"
CURRENT_PROBES_URL = RIPE_BASE_URL + "credits/income-items/"
ANCHORS_URL = RIPE_BASE_URL + "anchors/"
PROBES_URL = RIPE_BASE_URL + "probes/"
RIPE_STATS_ASN_NEIGHBOURS = "https://stat.ripe.net/data/asn-neighbours/data.json"
RIPE_STATS_ASN = "https://stat.ripe.net/data/as-overview/data.json"

"""RIPE RESPONSE FIELDS"""
# fields should be comma seperated for the fields query parameter, id and type is always included
WANTED_PROBE_FIELDS = "id,is_anchor,type,address_v4,address_v6,asn_v4,asn_v6,geometry,prefix_v4,prefix_v6,description"
WANTED_ANCHOR_FIELDS = "id,ip_v4,ipv6,as_v4,as_v6,geometry,prefix_v4,prefix_v6,fqdn"
WANTED_ANCHOR_MEASUREMENT_FIELDS = "id,type,interval,description"
WANTED_MEASUREMENT_FIELDS = "id,type,interval,description,target_ip,target,target_asn,target_prefix"

"""SUPPORTED MEASUREMENTS"""
SUPPORTED_TYPE_MEASUREMENTS = ('ping', 'traceroute')


class RipeInterface:

    @staticmethod
    def is_token_valid(token: str) -> bool:
        """Checks if the token exists in Ripe"""
        response = requests.get(url=CURRENT_PROBES_URL, params={'key': token})
        if response.status_code == 403:
            if response.json()['error']['detail'] == 'The provided API key does not exist':
                return False
        else:
            return True

    @staticmethod
    def get_anchors(asn_list: list) -> dict:
        """returns dictionary with as keys the input asn and as value a list of anchors
        if empty dict then there are no anchors found"""
        anchors_by_asn = defaultdict(list)
        for asn in asn_list:

            params = {"as_v4": asn}
            response = requests.get(url=ANCHORS_URL, params=params).json()
            results = response.get('results')
            if results:
                anchors_by_asn[asn].extend(results)
        return anchors_by_asn

    @staticmethod
    def get_anchoring_measurements(target_address: str) -> list:

        params = {
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_ip': target_address,
            'fields': WANTED_ANCHOR_MEASUREMENT_FIELDS
        }
        response = requests.get(MEASUREMENTS_URL, params=params).json()
        return [measurement for measurement in response['results'] if
                measurement['type'] in SUPPORTED_TYPE_MEASUREMENTS]

    @staticmethod
    def get_asn_host(asn: int):
        response = requests.get(RIPE_STATS_ASN, params={"resource": asn}).json()
        return {"holder": response['data']['holder']}


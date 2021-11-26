import requests

RIPE_BASE_URL = "https://atlas.ripe.net/api/v2/"
MEASUREMENTS_URL = RIPE_BASE_URL + "measurements/"
MY_MEASUREMENTS_URL = MEASUREMENTS_URL + "my/"
CURRENT_PROBES_URL = RIPE_BASE_URL + "credits/income-items/"
ANCHORS_URL = RIPE_BASE_URL + "anchors/"
PROBES_URL = RIPE_BASE_URL + "probes/"

# fields should be comma seperated for the fields query parameter, id and type is always included
WANTED_PROBE_FIELDS = "id,is_anchor,type,address_v4,address_v6,asn_v4,asn_v6,geometry,prefix_v4,prefix_v6,description"
WANTED_ANCHOR_FIELDS = "id,ip_v4,ipv6,as_v4,as_v6,geometry,prefix_v4,prefix_v6,fqdn"
WANTED_ANCHOR_MEASUREMENT_FIELDS = "id,type,interval,description"
WANTED_MEASUREMENT_FIELDS = "id,type,interval,description,target_ip,target,target_asn,target_prefix"

# the type of  measurements that we can put an alert on
SUPPORTED_TYPE_MEASUREMENTS = ('ping', 'traceroute')


class RipeInterface:

    @staticmethod
    def is_token_valid(token: str) -> bool:
        response = requests.get(url=RIPE_BASE_URL + "credits/income-items", params={'key': token})
        if response.status_code == 403:
            if response.json()['error']['detail'] == 'The provided API key does not exist':
                return False
        else:
            return True

    def __init__(self, token):
        self.token: str = token
        self.user_defined_measurements: list = self.get_user_defined_measurements()

    def get_probe_information(self, url=None, probe_id=None) -> dict:

        # status: 1, means we are only interested in probes that are connected.
        params = {"key": self.token, "fields": WANTED_PROBE_FIELDS, "status": 1}

        if probe_id:
            url = PROBES_URL + f"{probe_id}"
        response = requests.get(url, params=params).json()

        # probes data dont have a 'host' key, but the description refers to the host in most cases
        response['host'] = response.pop('description')
        return response

    def group_measurements_by_target(self, measurements) -> list:
        measurements_by_target = []

        for measurement in measurements:

            # check if the target is already known
            unknown = True
            measurement_target = {
                "target": measurement.pop("target"),
                "target_ip": measurement.pop("target_ip"),
                "target_asn": measurement.pop("target_asn"),
                "target_prefix": measurement.pop("target_prefix")
            }

            for target in measurements_by_target:

                if measurement_target['target_ip'] == target['target_ip']:
                    target['measurements'].append(measurement)
                    unknown = False
                    break

            if unknown:
                measurement_target["measurements"] = [measurement]
                measurements_by_target.append(measurement_target)

        measurements_by_target.sort(key=lambda target: len(target['measurements']), reverse=True)

        return measurements_by_target

    def get_targets(self, filter, value) -> list:

        measurements = []
        params = {'fields': WANTED_MEASUREMENT_FIELDS, 'key': self.token, 'status': 'Ongoing'}
        if filter == "host":
            params['target__startswith'] = value
        elif filter == "asn":
            params['target_asn'] = value
        elif filter == "ip_address":
            params['target_ip'] = value
        else:
            raise ValueError

        response = requests.get(url=MEASUREMENTS_URL, params=params).json()

        while True:

            measurements.extend([measurement for measurement in response['results'] if
                                 measurement['type'] in SUPPORTED_TYPE_MEASUREMENTS
                                 and measurement not in self.user_defined_measurements])
            next_url = response.get('next')

            if next_url:
                response = requests.get(url=next_url).json()
            else:
                break

        measurements_by_target = self.group_measurements_by_target(measurements)
        print(measurements_by_target)

        return measurements_by_target

    def get_anchoring_measurements(self, target_address: str) -> list:

        params = {
            'key': self.token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_ip': target_address,
            'fields': WANTED_ANCHOR_MEASUREMENT_FIELDS
        }
        response = requests.get(MEASUREMENTS_URL, params=params).json()
        return [measurement for measurement in response['results'] if
                measurement['type'] in SUPPORTED_TYPE_MEASUREMENTS]

    def get_user_defined_measurements(self):

        params = {
            "key": self.token,
            # "status": "Ongoing",
            "fields": WANTED_MEASUREMENT_FIELDS
        }
        response = requests.get(MY_MEASUREMENTS_URL, params=params).json()
        return [measurement for measurement in response['results'] if
                measurement['type'] in SUPPORTED_TYPE_MEASUREMENTS]

    def get_alertable_user_measurements_target(self, ip_address: str) -> list:

        if len(self.user_defined_measurements) > 0:
            return [measurement for measurement in self.user_defined_measurements
                    if measurement['target_ip'] == ip_address]
        else:
            return []

    def get_alertable_measurements_probe(self, probe: dict) -> dict:
        """Get alertable measurements that target probe"""

        relevant_measurements = {
            "user_defined_measurements": []
        }

        ip_v4 = probe.get("address_v4")
        ip_v6 = probe.get("address_v6")

        if ip_v4:
            relevant_measurements['user_defined_measurements'].extend(
                self.get_alertable_user_measurements_target(ip_v4))

        if ip_v6:
            relevant_measurements['user_defined_measurements'].extend(
                self.get_alertable_user_measurements_target(ip_v6))

        return relevant_measurements

    def get_alertable_measurements_anchor(self, anchor: dict) -> dict:

        # only anchoring measurements are relevant

        relevant_measurements = {
            "anchoring_measurements": [],
        }

        ip_v4 = anchor.get("address_v4")
        ip_v6 = anchor.get("address_v6")

        if ip_v4:
            relevant_measurements['anchoring_measurements'].extend(self.get_anchoring_measurements(ip_v4))

        if ip_v6:
            relevant_measurements['anchoring_measurements'].extend(self.get_anchoring_measurements(ip_v6))

        return relevant_measurements

    def get_user_targets(self, owned_anchors) -> list:

        anchor_ip_set = set()
        for anchor in owned_anchors:
            anchor_ip_set.add(anchor['address_v4'])
            anchor_ip_set.add(anchor['address_v6'])
        measurements = [measurement for measurement in self.user_defined_measurements
                        if measurement['target_ip'] not in anchor_ip_set]

        return self.group_measurements_by_target(measurements)

    def get_my_anchors_targets(self) -> dict:

        owned_anchors = self.get_owned_anchors()
        anchors_and_targets = {
            'anchors': owned_anchors,
            'targets': self.get_user_targets(owned_anchors)
        }

        return anchors_and_targets

    def get_owned_anchors(self) -> list:

        owned_anchors = []
        response = requests.get(url=CURRENT_PROBES_URL, params={'key': self.token}).json()
        income_groups: dict = response['groups']
        income_sources: list = [*income_groups['hosted_probes'], *income_groups['hosted_anchors'], *income_groups['sponsored_anchors']]

        for income_source in income_sources:
            anchor = self.get_probe_information(url=income_source['probe'])
            anchor.update(self.get_alertable_measurements_anchor(anchor))
            owned_anchors.append(anchor)

        return owned_anchors

    def get_owned_anchors_probes(self) -> dict:

        anchors_and_probes: dict = {"anchors": [], "probes": []}
        response = requests.get(url=CURRENT_PROBES_URL, params={'key': self.token}).json()
        income_groups: dict = response['groups']
        income_sources: list = [*income_groups['hosted_probes'], *income_groups['sponsored_probes'],
                                *income_groups['ambassador_probes'], *income_groups['hosted_anchors'],
                                *income_groups['sponsored_anchors']]

        for income in income_sources:
            probe_information = self.get_probe_information(url=income['probe'])

            # add related measurements to probe
            probe_information.update(self.get_alertable_measurements_probe(probe_information))

            if probe_information['is_anchor']:
                anchors_and_probes['anchors'].append(probe_information)
            else:
                anchors_and_probes['probes'].append(probe_information)

        return anchors_and_probes

    def search_systems(self, filter, value):

        if filter == "probe_id":
            probe = self.get_probe_information(probe_id=value)
            if probe['is_anchor']:
                probe.update(self.get_alertable_measurements_anchor(probe))
            else:
                probe.update(self.get_alertable_measurements_probe(probe))
            return probe
        else:
            return self.get_targets(filter, value)


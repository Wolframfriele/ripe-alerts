import requests

RIPE_BASE_URL = "https://atlas.ripe.net/api/v2/"

# fields should be comma seperated for the fields query parameter, id and type is always included
WANTED_PROBE_FIELDS = "id,is_anchor,address_v4,address_v6,asn_v4,asn_v6,geometry,prefix_v4,prefix_v6,description"
WANTED_MEASUREMENT_FIELDS = "id,type,description,target_ip"


def is_token_valid(token: str) -> bool:
    """check if given api-token is valid"""
    response = requests.get(url=RIPE_BASE_URL + "credits/income-items", params={'key': token})
    if response.status_code == 403:
        if response.json()['error']['detail'] == 'The provided API key does not exist':
            return False
    else:
        return True


def get_anchor_information(url=None, anchor_id=None) -> dict:
    if url:
        response = requests.get(url).json()
    else:
        response = requests.get(url=RIPE_BASE_URL + f"anchors/{anchor_id}").json()
    return response


def get_probe_information(url=None, probe_id=None) -> dict:
    if url:
        url = url + f"?fields={WANTED_PROBE_FIELDS}"
        response = requests.get(url).json()
    else:
        response = requests.get(url=RIPE_BASE_URL + f"probes/{probe_id}?fields={WANTED_PROBE_FIELDS}").json()

    return response


def get_anchoring_measurements(filters):
    response = requests.get(RIPE_BASE_URL + "measurements", params=filters).json()
    return [measurement for measurement in response['results'] if measurement['type'] == "ping"]


def get_user_defined_measurements(filters):
    response = requests.get(RIPE_BASE_URL + "measurements/my", params=filters).json()
    return [measurement for measurement in response['results'] if measurement['type'] == "ping"]


def get_relevant_measurements_for_probe(token: str, ip_v4, ip_v6, user_defined_measurements, anchor=True):
    """Algemene functie relevante metingen gekoppeld aan een bepaalde target uit ripe-atlas haalt, dit
    zijn de user defined measurements die als target de probe hebben of
    de anchoring measurements, de ip adressen representeren de probes"""

    relevant_measurements = {
        "anchoring_measurements": [],
        "user_defined_measurements": []
    }

    if len(user_defined_measurements) > 0:
        user_defined_measurements = [measurement for measurement in user_defined_measurements if measurement['type'] == "ping"]


    if ip_v4:
        filters = {
            'key': token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_ip': ip_v4,
            'fields': WANTED_MEASUREMENT_FIELDS
        }

        # get anchoring measurements
        if anchor:
            relevant_measurements['anchoring_measurements'].extend(get_anchoring_measurements(filters))

        # get user-defined measurements
        filters.pop('tags')
        if len(user_defined_measurements) > 0:
            relevant_measurements['user_defined_measurements'].extend([measurement for measurement in
                                                                       user_defined_measurements if
                                                                       measurement['target_ip'] == ip_v4])
        # relevant_measurements['user_defined_measurements'].extend(get_user_defined_measurements(filters))

    if ip_v6:
        filters = {
            'key': token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_ip': ip_v6,
            'fields': WANTED_MEASUREMENT_FIELDS
        }
        # get anchoring measurements
        if anchor:
            relevant_measurements['anchoring_measurements'].extend(get_anchoring_measurements(filters))
        filters.pop('tags')
        # get user-defined measurements
        if len(user_defined_measurements) > 0:
            relevant_measurements['user_defined_measurements'].extend([measurement for measurement in
                                                                       user_defined_measurements if
                                                                       measurement['target_ip'] == ip_v6])
        # relevant_measurements['user_defined_measurements'].extend(get_user_defined_measurements(filters))

    return relevant_measurements


def get_anchors_probes_with_token(key) -> dict:
    """
    Returns a dictionary with anchors and probes as keys, both contain a list of probes,
    a probe has two extra fields anchoring_measurements and user_defined_measurents these alerts that can be alerted on
    """

    anchors_and_probes: dict = {"anchors": [], "probes": []}
    response = requests.get(url=RIPE_BASE_URL + "credits/income-items", params={'key': key})
    if response.status_code != 200:
        return response.json()

    response = response.json()

    income_groups: dict = response['groups']
    hosted_probes: list = income_groups['hosted_probes']
    sponsored_probes: list = income_groups['sponsored_probes']
    ambassador_probes: list = income_groups['ambassador_probes']
    hosted_anchors: list = income_groups['hosted_anchors']
    sponsored_anchors: list = income_groups['sponsored_anchors']
    probes: list = [*hosted_probes, *sponsored_probes, *ambassador_probes, *hosted_anchors, * sponsored_anchors]

    user_defined_measurements = requests.get(RIPE_BASE_URL + "measurements/my",
                                             params={"key": key, "status": "Ongoing",
                                                     'fields': WANTED_MEASUREMENT_FIELDS}).json()['results']
    for probe in probes:
        probe_information = get_probe_information(url=probe['probe'])
        probe_information.update(get_relevant_measurements_for_probe(token=key, ip_v4=probe_information['address_v4'],
                                                                     ip_v6=probe_information['address_v6'],
                                                                     user_defined_measurements=user_defined_measurements, anchor=probe_information['is_anchor']))
        if probe_information['is_anchor']:
            anchors_and_probes['anchors'].append(probe_information)
        else:
            anchors_and_probes['probes'].append(probe_information)

    return anchors_and_probes


def search_probes(key, filter, value):
    anchors_and_probes: dict = {"anchors": [], "probes": []}

    if filter == "probe_id":
        probes = [get_probe_information(probe_id=value)]

    elif filter == "host":
        response = requests.get(url=RIPE_BASE_URL + "/anchors", params={'search': value, 'include': 'probe'}).json()
        results = response['results']

        # keep only the wanted fields of probes
        probes = [result['probe'] for result in results]
        probes = [{field: probe[field] for field in WANTED_PROBE_FIELDS.split(',')} for probe in probes]

    elif filter == "prefix":
        #check prefix_v4
        response: dict = requests.get(url=RIPE_BASE_URL + "/probes",
                                      params={'prefix_v4': value, 'fields': WANTED_PROBE_FIELDS}).json()
        results = response.get('results')
        if results:
            if len(response['results']) != 0:
                probes = response['results']
        #check prefix_v6
        else:
            response = requests.get(url=RIPE_BASE_URL + "/probes", params={'prefix_v6': value,
                                                                           'fields': WANTED_PROBE_FIELDS}).json()
            results = response.get('results')
            if results:
                probes = results
            else:
                raise ValueError
    else:
        response = requests.get(url=RIPE_BASE_URL + "/probes", params={filter: value,
                                                                       'fields': WANTED_PROBE_FIELDS}).json()
        probes = response.get('results')

    if probes:
        user_defined_measurements = requests.get(RIPE_BASE_URL + "measurements/my",
                                                 params={"key": key, "status": "Ongoing",
                                                         'fields': WANTED_MEASUREMENT_FIELDS}).json()['results']
        for probe in probes:
            probe.update(
                get_relevant_measurements_for_probe(token=key, ip_v4=probe['address_v4'],
                                                    ip_v6=probe['address_v6'],
                                                    user_defined_measurements=user_defined_measurements, anchor=probe['is_anchor']))

            if probe['is_anchor']:
                anchors_and_probes['anchors'].append(probe)
            else:
                anchors_and_probes['probes'].append(probe)
    else:
        raise ValueError
    return anchors_and_probes


def get_relevant_measurements(token: str, host: str = None, ip=None, asn=None):
    """Algemene functie relevante metingen gekoppeld aan een bepaalde target uit ripe-atlas haalt, dit
    zijn de user defined measurements die als target de probe hebben of
    de anchoring measurements, de ip adressen representeren de probes"""

    relevant_measurements = {
        "anchoring_measurements": [],
        "user_defined_measurements": []
    }
    if host is None and ip is None and asn is None:
        return relevant_measurements

    if host:
        filters = {
            'key': token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target': host,
            'fields': WANTED_MEASUREMENT_FIELDS
        }
    if ip:
        filters = {
            'key': token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_ip': ip,
            'fields': WANTED_MEASUREMENT_FIELDS
        }
    if asn:
        filters = {
            'key': token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_asn': asn,
            'fields': WANTED_MEASUREMENT_FIELDS
        }


    # get anchoring measurements
    response = requests.get(RIPE_BASE_URL + "measurements", params=filters).json()
    anchoring_measurements = response['results']
    relevant_measurements['anchoring_measurements'] = [measurement for measurement in anchoring_measurements if measurement['type'] == "ping"]

    # get user-defined measurements
    filters.pop('tags')
    response = requests.get(RIPE_BASE_URL + "measurements/my", params=filters).json()
    user_defined_measurements = response['results']
    relevant_measurements['user_defined_measurements'] = [measurement for measurement in user_defined_measurements if measurement['type'] == "ping"]
    return relevant_measurements

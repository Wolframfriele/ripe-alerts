import requests

RIPE_BASE_URL = "https://atlas.ripe.net/api/v2/"


def is_token_valid(token: str) -> bool:
    """check if given api-token is valid"""
    if requests.get(url=RIPE_BASE_URL + "credits/income-items", params={'key': token}).status_code == 403:
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
        response = requests.get(url).json()
    else:
        response = requests.get(url=RIPE_BASE_URL + f"probes/{probe_id}").json()
    return response


def search_probes(filter, value):
    anchors_and_probes: dict = {"anchors": [], "probes": []}
    if filter == "probe_id":
        response = get_probe_information(probe_id=value)
        return response
    elif filter == "host":
        response = requests.get(url=RIPE_BASE_URL + "/anchors", params={'search': value, 'include': 'probe'}).json()
        results = response['results']
        probes = [result['probe'] for result in results]
    elif filter == "prefix":
        #check prefix_v4
        response: dict = requests.get(url=RIPE_BASE_URL + "/probes", params={'prefix_v4': value}).json()
        results = response.get('results')
        if results:
            if len(response['results']) != 0:
                probes = response['results']
        #check prefix_v6
        else:
            response = requests.get(url=RIPE_BASE_URL + "/probes", params={'prefix_v6': value}).json()
            results = response.get('results')
            if results:
                probes = results
            else:
                raise ValueError
    else:
        response = requests.get(url=RIPE_BASE_URL + "/probes", params={filter: value}).json()
        probes = response.get('results')

    if probes:
        for probe in probes:
            if probe['is_anchor']:
                anchors_and_probes['anchors'].append(probe)
            else:
                anchors_and_probes['probes'].append(probe)
    else:
        raise ValueError
    return anchors_and_probes


def get_anchors_probes_with_token(key) -> dict:
    """
    Returns a dictionary with anchors and probes as keys they refer to a list of connected anchors or probes owned by
    the user
    """
    anchors_and_probes: dict = {"anchors": [], "probes": []}
    response = requests.get(url=RIPE_BASE_URL + "credits/income-items", params={'key': key})
    if response.status_code != 200:
        return response.json()

    response = response.json()
    print(response)

    income_groups: dict = response['groups']
    hosted_probes: list = income_groups['hosted_probes']
    sponsored_probes: list = income_groups['sponsored_probes']
    ambassador_probes: list = income_groups['ambassador_probes']
    hosted_anchors: list = income_groups['hosted_anchors']
    sponsored_anchors: list = income_groups['sponsored_anchors']
    probes: list = [*hosted_probes, *sponsored_probes, *ambassador_probes, *hosted_anchors, * sponsored_anchors]

    for probe in probes:
        probe_information = get_probe_information(url=probe['probe'])
        if probe_information['is_anchor']:
            anchors_and_probes['anchors'].append(probe_information)
        else:
            anchors_and_probes['probes'].append(probe_information)

    return anchors_and_probes


def get_relevant_measurements(token: str, host: str = None, ip=None, asn=None):
    """relevante metingen gekoppeld aan de probe, zijn de user defined measurements die als target de probe hebben of
    de anchoring measurements, de ip adressen representeren de probes"""

    relevant_measurements = {
        "anchoring_measurements": [],
        "user_defined_measurements": []
    }
    if host:
        filters = {
            'key': token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target': host
        }
    if ip:
        filters = {
            'key': token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_ip': ip
        }
    if asn:
        filters = {
            'key': token,
            'tags': 'anchoring',
            'status': 'Ongoing',
            'target_asn': asn
        }


    # get anchoring measurements
    response = requests.get(RIPE_BASE_URL + "measurements", params=filters).json()
    anchoring_measurements = response['results']
    relevant_measurements['anchoring_measurements'] = anchoring_measurements

    # get user-defined measurements
    filters.pop('tags')
    response = requests.get(RIPE_BASE_URL + "measurements/my", params=filters).json()
    user_defined_measurements = response['results']
    relevant_measurements['user_defined_measurements'] = user_defined_measurements
    return relevant_measurements

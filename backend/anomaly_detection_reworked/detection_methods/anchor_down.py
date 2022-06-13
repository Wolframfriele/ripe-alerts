from typing import List

import requests

from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class AnchorDown(DetectionMethod):
    """
    This Detection Method (algorithm) has not been finished. However, all methods work as supposed to.
    """

    def __init__(self):
        self.measurement_ids = List[int]

    def on_result_response(self, data: dict):
        measurement_id = data['msm_id']
        if measurement_id not in self.measurement_ids:
            self.measurement_ids.append(measurement_id)
            print(type(measurement_id))
            print("Added ID: " + str(measurement_id))
        # LIST.
        # GET MSM ID -> ASN -> ANCHORS ->
        # GET ALL FQDN DOMAINS
        # PING ALL DOMAINS EVERY 30 SECONDS
        # IF NO RESPONSE -> CREATE AN ANOMALY
        #
        pass

    def on_startup_event(self):
        self.measurement_ids = []
        asn = self.get_autonomous_system_number(measurement_id=23103873)
        meta_anchors = self.get_anchor_metadata(asn)
        for meta in meta_anchors:
            print(meta.description)
            print(meta.asn_v6)
            print(meta.is_anchor)
            print(meta.id)
            print(meta.address_v4)
            print(meta.country_code)
            print(meta.prefix_v6)
        print("Anchor Down loaded")
        pass

    @property
    def get_measurement_type(self) -> MeasurementType:
        return MeasurementType.PING

    @staticmethod
    def get_autonomous_system_number(measurement_id: int) -> int:
        """ Returns the Autonomous System Number (ASN) based of the Measurement ID
            by doing a GET Request to RIPE ATLAS. """
        uri = 'https://atlas.ripe.net/api/v2/measurements/' + str(measurement_id) + "/"
        response = requests.get(uri).json()
        return int(response.get('target_asn'))

    @staticmethod
    def get_anchor_metadata(target_asn: int):
        uri = 'https://atlas.ripe.net/api/v2/probes/'
        params = {"asn_v4": target_asn, "is_anchor": True}
        response = requests.get(uri, params=params).json()
        results = response.get('results')
        meta_anchors = []
        for x in results:
            print(x)
            meta_anchor = MetaAnchor(**x)
            meta_anchors.append(meta_anchor)
        print(123132)
        print(str(len(meta_anchors)))
        return meta_anchors
        # return int(response.get('count'))


class MetaAnchor:

    def __init__(self, address_v4, address_v6, asn_v4, asn_v6, country_code, description, first_connected, id, is_anchor
                 , is_public, last_connected, prefix_v6, prefix_v4
                 ):
        self.address_v4 = address_v4
        self.address_v6 = address_v6
        self.asn_v4 = asn_v4
        self.asn_v6 = asn_v6
        self.country_code = country_code
        self.description = description
        self.first_connected = first_connected
        self.id = id
        self.is_anchor = is_anchor
        self.is_public = is_public
        self.last_connected = last_connected
        self.prefix_v6 = prefix_v6
        self.prefix_v4 = prefix_v4
        # self.geometry: dict = geometry
        # # self.# {
        # # self.#     type Point
        # # self.#     coordinates: [
        # # self.#         5.1205
        # # self.#         52.0895
        # # self.#     ]
        # # self.# }
        # self.status: dict
        # # self.# {
        # # self.#     id: 3
        # # self.#     name: Abandoned
        # # self.#     since: 2021-06-22T12:53:56Z
        # # self.# }
        # self.status_since: int
        # # self.# 1624366436
        # self.tags: dict
        # # self.# [
        # # self.#     {
        # # self.#         name: system: Anchor
        # # self.#         slug: system-anchor
        # # self.#     }
        # # self.#     {
        # # self.#         name: system: IPv4 Capable
        # # self.#         slug: system-ipv4-capable
        # # self.#     }
        # # self.#     {
        # # self.#         name: system: IPv6 Capable
        # # self.#         slug: system-ipv6-capable
        # # self.#     }
        # # self.#     {
        # # self.#         name: system: DNS problem suspected
        # # self.#         slug: system-dns-problem-suspected
        # # self.#     }
        # # self.#     {
        # # self.#         name: system: V2 Soekris
        # # self.#         slug: system-v2-soekris
        # # self.#     }
        # # self.# ]
        # self.total_uptime: int
        # self.type: str

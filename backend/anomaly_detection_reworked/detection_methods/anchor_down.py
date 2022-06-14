import datetime
import enum
import threading
from typing import List

import dateutil.parser
import requests

from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class AnchorDown(DetectionMethod):
    """
    This Detection Method (algorithm) has not been finished. However, all methods work as supposed to.
    """

    def __init__(self):
        self.measurement_ids: List[int] = []
        self.autonomous_system_number: int = 0
        self.analyzer_started: bool = False

    def on_result_response(self, data: dict):
        measurement_id = data['msm_id']
        if measurement_id not in self.measurement_ids and not self.analyzer_started:
            self.measurement_ids.append(measurement_id)
            self.autonomous_system_number = self.get_autonomous_system_number(measurement_id=measurement_id)
            self.start_analyzer()

    def analyzer(self, autonomous_system_number: int, event: threading.Event):
        while not event.is_set():
            # self.get_probe_metadata(self.autonomous_system_number)
            print("Hi there for the " + str(autonomous_system_number) + " time!")
            event.wait(2)

    def start_analyzer(self):
        if not self.analyzer_started:
            event = threading.Event()
            thread = threading.Thread(target=self.analyzer, args=(self.autonomous_system_number, event), daemon=True)
            thread.start()

    def on_startup_event(self):
        asn = self.get_autonomous_system_number(measurement_id=23103873)
        meta_anchors = self.get_probe_metadata(asn)
        self.start_analyzer()
        for meta in meta_anchors:
            print(str(meta.status.id) + " " + str(meta.status.name))
        print("Anchor Down Detection Method loaded")

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
    def get_probe_metadata(target_asn: int):
        uri = 'https://atlas.ripe.net/api/v2/probes/'
        params = {"asn_v4": target_asn, "is_anchor": True}
        response = requests.get(uri, params=params).json()
        results = response.get('results')
        meta_probes: List[MetaProbe] = []
        for x in results:
            meta_anchor = MetaProbe(**x)
            meta_probes.append(meta_anchor)
        return meta_probes


class ConnectionStatus(enum.Enum):
    NEVER_CONNECTED = 0
    CONNECTED = 1
    DISCONNECTED = 2
    ABANDONED = 3

    @staticmethod
    def convert(enum_str: str):
        if enum_str == 'Never Connected':
            return ConnectionStatus.NEVER_CONNECTED
        elif enum_str == 'Connected':
            return ConnectionStatus.CONNECTED
        elif enum_str == 'Disconnected':
            return ConnectionStatus.DISCONNECTED
        elif enum_str == 'Abandoned':
            return ConnectionStatus.ABANDONED


class Status:

    def __init__(self, id, name, since):
        """ A parsed JSON object containing
            id: The connection status ID for this probe (integer [0-3]),
            name: The connection status as String [Never Connected, Connected, Disconnected, Abandoned],
            since: The datetime of the last change in connection status."""
        self.id = id
        self.name = ConnectionStatus.convert(name)
        self.since = dateutil.parser.isoparse(since)


class MetaProbe:

    def __init__(self, address_v4, address_v6, asn_v4, asn_v6, country_code, description, first_connected, id, is_anchor
                 , is_public, last_connected, prefix_v6, prefix_v4, geometry, status, status_since, tags, total_uptime,
                 type):
        """
        RIPE Atlas Probes Resource. Note: An Anchor is also a Probe. Probes however are not always Anchors.
        For more: https://beta-docs.atlas.ripe.net/apis/metadata-reference/#probes
        """
        self.address_v4 = address_v4
        self.address_v6 = address_v6
        self.asn_v4 = asn_v4
        self.asn_v6 = asn_v6
        self.country_code = country_code
        self.description = description
        self.first_connected = first_connected
        self.geometry = geometry
        self.id = id
        self.is_anchor = is_anchor
        self.is_public = is_public
        self.last_connected = datetime.datetime.fromtimestamp(last_connected)
        self.prefix_v4 = prefix_v4
        self.prefix_v6 = prefix_v6
        self.status = Status(**status)
        self.status_since = datetime.datetime.fromtimestamp(status_since)
        self.tags = tags
        self.total_uptime = total_uptime
        self.type = type

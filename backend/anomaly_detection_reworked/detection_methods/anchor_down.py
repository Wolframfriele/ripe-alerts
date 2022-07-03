import datetime
import enum
import threading
from typing import List
from django.utils import timezone
import dateutil.parser
import requests

from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.measurement_type import MeasurementType


class AnchorDown(DetectionMethod):
    """
    Anchor Down Detection Method (algorithm) used to find anomalies.
    It checks every 15 seconds if the Anchor/Probe went offline .
    """

    def __init__(self):
        self.detection_method_name = "Anchor Down"
        self.detection_method_id = None
        self.probes = None
        self.measurement_ids: List[int] = []
        self.autonomous_system_number: int = 0
        self.analyzer_started: bool = False
        self.interval = 30

    def on_result_response(self, data: dict):
        """ Method that will be called every time we receive a new result from the RIPE Streaming API.
            We retrieve the measurement ID and Autonomous System Number that belongs to it and start the analyzer. """
        measurement_id = data['msm_id']
        if measurement_id not in self.measurement_ids and not self.analyzer_started:
            self.measurement_ids.append(measurement_id)
            self.autonomous_system_number = self.get_autonomous_system_number(measurement_id=measurement_id)
            self.start_analyzer()

    def analyzer(self, autonomous_system_number: int, event: threading.Event):
        """ The Analyzer Method analyzes all incoming data to conclude if there was an anomaly or not.
            This Method is called every (self.interval) seconds. """
        while not event.is_set():
            event.wait(self.interval)
            if self.probes is None:
                self.probes = self.get_probes_metadata(self.autonomous_system_number)
                return
            else:
                old_probes = self.probes
                new_probes = self.get_probes_metadata(self.autonomous_system_number)
                for (old_probe, new_probe) in zip(old_probes, new_probes):
                    assert isinstance(old_probe, MetaProbe)
                    assert isinstance(new_probe, MetaProbe)
                    if new_probe.status.name == ConnectionStatus.DISCONNECTED:
                        # If there isn't already an Anomaly containing the probe address past 24 hours. Don't show.
                        if not self.has_anomaly(msg="Anchor is offline.", ip_addresses=new_probe.address_v4):
                            self.create_anomaly(msg="Anchor is offline.", ip_addresses=new_probe.address_v4)
                    elif new_probe.status.name == ConnectionStatus.NEVER_CONNECTED:
                        # To prevent duplicates messages.
                        if not self.has_anomaly(msg="Anchor never connected.", ip_addresses=new_probe.address_v4):
                            self.create_anomaly(msg="Anchor never connected.", ip_addresses=new_probe.address_v4)
                    elif new_probe.status.name == ConnectionStatus.ABANDONED:
                        # To prevent duplicates messages.
                        if not self.has_anomaly(msg="Anchor has been abandoned.", ip_addresses=new_probe.address_v4):
                            self.create_anomaly(msg="Anchor has been abandoned.", ip_addresses=new_probe.address_v4)
                self.probes = new_probes

    def start_analyzer(self):
        """ To start the analyzer and have it called in an interval, we'll need a thread. In our case,
            running one instance is enough. """
        if not self.analyzer_started:
            event = threading.Event()
            thread = threading.Thread(target=self.analyzer, args=(self.autonomous_system_number, event), daemon=True)
            thread.start()

    def on_startup_event(self):
        """ Method that will be called once the detection method has been loaded.
            Create an Anchor Down Detection Method and save it to the database. """
        from database.models import DetectionMethod as DetectionMethodDB
        if not DetectionMethodDB.objects.filter(type=self.detection_method_name).exists():
            detection_method = DetectionMethodDB.objects.create(type=self.detection_method_name,
                                                                description="Checks if the Anchor went offline "
                                                                            "every " + str(self.interval) + " seconds.")
            detection_method.save()

    @property
    def get_measurement_type(self) -> MeasurementType:
        """ Property which will be used to select corresponding Measurement IDs. """
        return MeasurementType.PING

    @property
    def describe(self) -> tuple:
        return {
            "type": "Anchor Down",
            "Description": "The detector checks if the anchors of the user have suddenly gone down."
        }

    def has_anomaly(self, msg: str, ip_addresses: str) -> bool:
        """ Every N seconds, we check if the Anchor went offline. To prevent duplicate messages, we first check if
            there already exists an anomaly like it in the database. And return it to the user. """
        from database.models import Anomaly
        if msg == "Anchor has been abandoned." or msg == "Anchor never connected.":
            return Anomaly.objects.filter(description=msg, ip_address=ip_addresses).exists()
        elif msg == "Anchor is offline.":
            past_24_hours = timezone.now() - datetime.timedelta(days=1)
            return Anomaly.objects.filter(description=msg,
                                          ip_address=ip_addresses, time__gte=past_24_hours).exists()

    def create_anomaly(self, msg: str, ip_addresses: str):
        """ This method is used to create anomalies to save to the database. """
        from database.models import Setting, AutonomousSystem, Anomaly, MeasurementType
        from database.models import DetectionMethod as DetectionMethodDB
        time = timezone.now()
        prediction_value = False
        setting = Setting.get_user_settings('admin')
        method = DetectionMethodDB.objects.get(type=self.detection_method_name)
        Anomaly.objects.create(time=time, ip_address=ip_addresses,
                               autonomous_system=AutonomousSystem.objects.get(setting_id=setting.id),
                               description=msg,
                               measurement_type=MeasurementType.PING,
                               detection_method=method,
                               mean_increase=0,
                               anomaly_score=4.0, prediction_value=prediction_value,
                               asn=self.autonomous_system_number)

    @staticmethod
    def get_autonomous_system_number(measurement_id: int) -> int:
        """ Returns the Autonomous System Number (ASN) based of the Measurement ID
            by doing a GET Request to RIPE ATLAS. """
        uri = 'https://atlas.ripe.net/api/v2/measurements/' + str(measurement_id) + "/"
        response = requests.get(uri).json()
        return int(response.get('target_asn'))

    @staticmethod
    def get_probes_metadata(target_asn: int):
        """ Makes a GET request to RIPE ATLAS to get the latest info of our Anchor. """
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
    """ Enum which is used in the Status Class. """
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

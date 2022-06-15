import threading
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from anomaly_detection_reworked.anomaly_detection import AnomalyDetection
from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.detection_methods.anchor_down import AnchorDown
from anomaly_detection_reworked.detection_methods.delay_from_country import DelayFromCountry
from anomaly_detection_reworked.detection_methods.entry_point_delay import EntryPointDelay
from anomaly_detection_reworked.detection_methods.neighbor_network_delay import NeighborNetworkDelay
from anomaly_detection_reworked.detection_methods.route_change import RouteChange
from anomaly_detection_reworked.measurement_result_stream import MeasurementResultStream
from anomaly_detection_reworked.measurement_type import MeasurementType
from database.models import Setting
from ripe_interface.api import set_autonomous_system_setting
from ripe_interface.api_schemas import ASNumber


class TestDetectionMethods(TestCase):
    """ Test module for the Detection Methods package. """

    def setUp(self):
        """ Create a list of all detection methods and verify them later. """
        self.detection_methods = [EntryPointDelay(), AnchorDown(), RouteChange(), NeighborNetworkDelay(),
                                  DelayFromCountry()]

    def test_detection_method_valid_success(self):
        """ Test all given detection methods.
            A detection method is valid when it inherited from Detection Method and has all methods implemented.
        """
        for detection_method in self.detection_methods:
            self.assertIsInstance(detection_method, DetectionMethod)

            self.assertTrue(hasattr(detection_method, 'on_startup_event'), True)
            self.assertTrue(hasattr(detection_method, 'on_result_response'), True)
            self.assertTrue(hasattr(detection_method, 'get_measurement_type'), True)
            self.assertIsInstance(detection_method.get_measurement_type, MeasurementType)
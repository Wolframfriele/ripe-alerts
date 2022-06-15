from django.test import TestCase

from anomaly_detection_reworked.anomaly_detection import AnomalyDetection
from anomaly_detection_reworked.detection_methods.anchor_down import AnchorDown
from anomaly_detection_reworked.detection_methods.delay_from_country import DelayFromCountry
from anomaly_detection_reworked.detection_methods.entry_point_delay import EntryPointDelay
from anomaly_detection_reworked.detection_methods.neighbor_network_delay import NeighborNetworkDelay
from anomaly_detection_reworked.detection_methods.route_change import RouteChange


class TestAnomalyDetectionApp(TestCase):
    """ Test module for the Anomaly Detection app. """

    def setUp(self):
        """ Create an Anomaly Detection App instance and add all existing detection methods.
            Later, verify if all detection methods are added correctly. """
        self.anomaly_detection = AnomalyDetection()

        self.anomaly_detection.add_detection_method(EntryPointDelay())
        self.anomaly_detection.add_detection_method(AnchorDown())
        self.anomaly_detection.add_detection_method(RouteChange())
        self.anomaly_detection.add_detection_method(NeighborNetworkDelay())
        self.anomaly_detection.add_detection_method(DelayFromCountry())

        self.all_expected_methods = [EntryPointDelay(), AnchorDown(), RouteChange(), NeighborNetworkDelay(),
                                     DelayFromCountry()]

    def test_detection_method_list_success(self):
        """ Verify if all 5 Detection Methods have been added correctly with add_detection_method() """
        self.assertCountEqual(self.all_expected_methods, self.anomaly_detection.methods.values())

    def test_detection_method_list_empty_success(self):
        """ Remove all Detection Methods with remove_detection_method() and assert if it has been removed properly.
            We create a copy to prevent a RuntimeError: dictionary changed size during iteration.
        """
        methods_copy = list(self.anomaly_detection.methods.values()).copy()
        self.assertNotEqual(len(methods_copy), 0)  # Detection Method List must not be empty.
        for method in methods_copy:
            self.anomaly_detection.remove_detection_method(method)
            self.assertEqual(True, bool(method not in self.anomaly_detection.methods.values()))

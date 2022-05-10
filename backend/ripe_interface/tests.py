import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone

from database.models import Setting, AutonomousSystem, DetectionMethod, Anomaly, MeasurementType, Feedback
from ripe_interface.api import set_autonomous_system_setting
from ripe_interface.api_schemas import ASNumber
from ripe_interface.requests import RipeRequests


class RipeRequestTest(TestCase):
    """ Test module for all RipeRequests functions """

    def setUp(self):
        self.invalid_asn = 0  # This will always be an invalid Autonomous System Number.
        self.valid_asn = 1103  # A valid ASN with multiple anchors.
        self.invalid_target_address = "194.171.96.34"  # Target address of ASN1104 (which consists of probes only)
        self.valid_target_address = "195.169.125.10"  # Target address of ASN1103

    def test_get_anchors_invalid(self):
        total_anchors = len(RipeRequests.get_anchors(self.invalid_asn))
        self.assertEqual(total_anchors, 0)

    def test_get_anchors_valid(self):
        anchors = RipeRequests.get_anchors(self.valid_asn)
        total_anchors = len(anchors)
        self.assertNotEquals(total_anchors, 0)

    def test_autonomous_system_exist(self):
        self.assertEqual(RipeRequests.autonomous_system_exist(self.invalid_asn), False)
        self.assertEqual(RipeRequests.autonomous_system_exist(self.valid_asn), True)

    def test_get_anchoring_measurements_invalid(self):
        total_measurements = len(RipeRequests.get_anchoring_measurements(self.invalid_target_address))
        self.assertEqual(total_measurements, 0)

    def test_get_anchoring_measurements_valid(self):
        total_measurements = len(RipeRequests.get_anchoring_measurements(self.valid_target_address))
        self.assertNotEquals(total_measurements, 0)


class APITestSetAutonomousSystemSetting(TestCase):
    """ Test module for POST set/asn/{asn_number} API Endpoint """

    def setUp(self):
        self.client = Client()
        self.valid_asn = 1103
        self.invalid_asn = 1
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        Setting.objects.create(user=user)

    def test_set_autonomous_system_setting_valid(self):
        response = self.client.post('/api/asn/' + str(self.valid_asn))
        result = response.json()
        monitoring_possible = result.get('monitoring_possible')
        host_is_empty = not bool(result.get('host'))
        message = result.get('message')
        self.assertEqual(monitoring_possible, True)
        self.assertEqual(host_is_empty, False)
        self.assertEqual(message, "Success!")
        self.assertEqual(response.status_code, 200)

    def test_set_autonomous_system_setting_invalid(self):
        response = self.client.post('/api/asn/' + str(self.invalid_asn))
        result = response.json()
        monitoring_possible = result.get('monitoring_possible')
        host = result.get('host')
        message = result.get('message')
        self.assertEqual(monitoring_possible, False)
        self.assertEqual(host, None)
        self.assertIn("ASN", message)
        self.assertIn("does not exist!", message)
        self.assertEquals(response.status_code, 404)


class APITestListAnomalies(TestCase):
    """ Test module for GET set/asn/anomaly API Endpoint """

    def setUp(self):
        """ Create a user and 3 anomalies to their list. """
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        setting = Setting.objects.create(user=user)
        self.asn = ASNumber()
        self.asn.value = 1103
        self.response = set_autonomous_system_setting(request=None, asn=self.asn)
        self.json_response = json.loads(self.response.content)

        self.time = timezone.now()
        self.time_formatted = str(self.time.year) + "-" + str(self.time.month) + "-" + str(self.time.day) + \
                              " " + str(self.time.hour) + ":" + str(self.time.minute) + ":" + str(self.time.second)
        self.ip_addresses = "localhost, google.com"
        self.ip_addresses_formatted = str(self.ip_addresses).replace(' ', '').split(",")
        self.description = "Ping above 100ms"
        self.measurement_type = MeasurementType.TRACEROUTE
        self.mean_increase = 2.1
        self.anomaly_score = 4.0
        self.prediction_value = False
        self.detection_method = DetectionMethod.objects.create(type="ipv6 traceroute", description="a1 algorithm")
        anomaly = Anomaly.objects.create(time=self.time, ip_address=self.ip_addresses,
                                         autonomous_system=AutonomousSystem.objects.get(setting_id=setting.id),
                                         description=self.description,
                                         measurement_type=self.measurement_type, detection_method=self.detection_method,
                                         mean_increase=self.mean_increase,
                                         anomaly_score=self.anomaly_score, prediction_value=self.prediction_value,
                                         asn=self.asn.value)
        anomaly.pk = None
        anomaly.save()  # Duplicate the anomaly
        anomaly.pk = None
        anomaly.save()  # Duplicate the anomaly again

    def test_response_valid(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.json_response['monitoring_possible'], True)
        self.assertEqual(self.json_response['message'], "Success!")

    def test_list_anomalies(self):
        self.client = Client()
        response = self.client.get("/api/asn/anomaly")
        result = response.json()
        self.assertEqual(result.get('count'), 3)
        anomalies = result.get('items')
        _id = 0
        _feedback = None
        for anomaly in anomalies:
            _id += 1
            _feedback = Feedback.get_feedback(_id)
            self.assertEqual(anomaly['id'], _id)
            self.assertEqual(anomaly['timestamp'], self.time_formatted)
            self.assertEqual(anomaly['ip_addresses'], self.ip_addresses_formatted)
            self.assertEqual(anomaly['description'], self.description)
            self.assertEqual(anomaly['measurement_type'], self.measurement_type)
            self.assertEqual(anomaly['detection_method']['id'], self.detection_method.id)
            self.assertEqual(anomaly['detection_method']['type'], self.detection_method.type)
            self.assertEqual(anomaly['detection_method']['description'], self.detection_method.description)
            self.assertEqual(anomaly['mean_increase'], self.mean_increase)
            self.assertEqual(anomaly['anomaly_score'], self.anomaly_score)
            self.assertEqual(anomaly['prediction_value'], self.prediction_value)
            self.assertEqual(anomaly['asn'], self.asn.value)
            self.assertEqual(anomaly['feedback'], _feedback)


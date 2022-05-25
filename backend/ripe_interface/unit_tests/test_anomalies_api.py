import json
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone

from database.models import Setting, AutonomousSystem, DetectionMethod, Anomaly, MeasurementType, Feedback
from ripe_interface.api import set_autonomous_system_setting
from ripe_interface.api_schemas import ASNumber


class APITestListAnomalies(TestCase):
    """ Test module for GET /api/anomalies endpoint. """

    def setUp(self):
        """ Add a user and a user settings file to the database. Next, create 3 anomalies add them to the user.
            Later, verify all 3 anomalies. """
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        setting = Setting.objects.create(user=user)
        self.asn = ASNumber()
        self.asn.value = 1103
        self.response = set_autonomous_system_setting(request=None, asn=self.asn)
        self.json_response = json.loads(self.response.content)
        # Specify the variables for the anomaly, so we can check them afterwards.
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
                                         asn=self.asn.value)  # 1st anomaly added to the database.
        anomaly.pk = None
        anomaly.save()  # Duplicate the anomaly (2nd anomaly)
        anomaly.pk = None
        anomaly.save()  # Duplicate the anomaly again (3rd anomaly)

    def test_response_success(self):
        """ Before verifying the anomalies, first check whether we got:
            the correct http status code, monitoring_possible set to true and a 'success' message."""
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.json_response['monitoring_possible'], True)
        self.assertEqual(self.json_response['message'], "Success!")

    def test_list_anomalies_success(self):
        """ A valid JSON Response has been returned, next up check if the 3 anomalies we inserted have been retrieved
            correctly. """
        self.client = Client()
        response = self.client.get("/api/anomalies/")
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

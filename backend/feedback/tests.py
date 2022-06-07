import json
from tkinter import N
from urllib import response
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from matplotlib.font_manager import json_load
from database.models import Setting, AutonomousSystem, DetectionMethod, Anomaly, MeasurementType, Feedback

from feedback.api import save_feedback
from feedback.api_schema import FeedbackFormat
from ripe_interface.api import set_autonomous_system_setting
from ripe_interface.api_schemas import ASNumber

class FeedbackApiTest(TestCase):
    """ Test module for all RipeRequests functions """

    def setUp(self):
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        setting = Setting.objects.create(user=user)
        self.asn = ASNumber()
        self.asn.value = 1103
        set_autonomous_system_setting(request=None, asn=self.asn)

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
        anomaly.save()

        self.feedback = FeedbackFormat()
        self.response = save_feedback(request=None, data=self.feedback)
        self.json_response = json.loads(self.response.content)

        self.bad_feedback = FeedbackFormat(anomaly_id=5, user_feedback=True)
        self.bad_response = save_feedback(request=None, data=self.bad_feedback)
        self.bad_json_response = json.loads(self.bad_response.content)


    def test_response_valid(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.json_response['message'], f"The feedback for anomaly {self.feedback.anomaly_id} has been succesfully saved!")

    def test_response_invalid(self):
        self.assertEqual(self.bad_response.status_code, 404)
        self.assertEqual(self.bad_json_response['message'], f"Failed, anomaly {self.bad_feedback.anomaly_id} does not exists!")
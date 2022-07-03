import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from database.models import Setting, AutonomousSystem, DetectionMethod, Anomaly, MeasurementType, Feedback
from feedback.api import save_feedback
from feedback.api_schema import FeedbackFormat
from feedback.feedback_engine import FeedbackEngine
from anomaly_detection_reworked.anomaly_object import AnomalyObject
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


class TestFeedbackEngine(TestCase):
    """Test module for the feedback engine."""
    def setUp(self) -> None:
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        self.setting = Setting.objects.create(user=user)
        self.asn = ASNumber()
        self.asn.value = 1103
        set_autonomous_system_setting(request=None, asn=self.asn)
        self.feedback_engine = FeedbackEngine()
        self.time = timezone.now()
        # self.time_formatted = str(self.time.year) + "-" + str(time.month) + "-" + str(time.day) + \
        #                       " " + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)
        self.ip_address = "localhost"
        self.description = "Dummy data"
        self.measurement_type = MeasurementType.TRACEROUTE
        self.prediction_value = True
        self.detection_method = DetectionMethod.objects.create(type="Dummy Detector", description="A Dummy Detection Method")
        return super().setUp()

    def add_anomalies(self) -> None:
        anomaly_values = [
            {"mean_increase": 2, "anomaly_score": 20, "feedback": False},
            {"mean_increase": 5.3, "anomaly_score": 33, "feedback": False},
            {"mean_increase": 1.1, "anomaly_score": 28, "feedback": False},
            {"mean_increase": 10, "anomaly_score": 15, "feedback": False},
            {"mean_increase": 3, "anomaly_score": 50, "feedback": False},
            {"mean_increase": 8, "anomaly_score": 16, "feedback": False},
            {"mean_increase": 80, "anomaly_score": 90, "feedback": True},
            {"mean_increase": 50, "anomaly_score": 80, "feedback": True},
            {"mean_increase": 44, "anomaly_score": 90, "feedback": True},
            {"mean_increase": 89, "anomaly_score": 55, "feedback": True},
            {"mean_increase": 52, "anomaly_score": 91, "feedback": True},
            {"mean_increase": 63, "anomaly_score": 74, "feedback": True},
        ]
        for data in anomaly_values:
            anomaly = Anomaly.objects.create(time=self.time,
                                            ip_address=self.ip_address,
                                            autonomous_system=AutonomousSystem.objects.get(setting_id=self.setting.id),
                                            description=self.description,
                                            measurement_type=self.measurement_type,
                                            detection_method=self.detection_method,
                                            mean_increase=data["mean_increase"],
                                            anomaly_score=data["anomaly_score"],
                                            prediction_value=self.prediction_value,
                                            asn=self.asn.value)
            anomaly.save()
            Feedback.objects.create(anomaly=anomaly, response=data["feedback"])

    def test_train_no_samples(self):
        """
        Check if the training fails when there are not enough samples (points of feedback)
        """
        self.assertEqual(self.feedback_engine.train(), False)

    def test_train(self):
        """
        Check if training succeeds with enough samples.
        """
        self.add_anomalies()
        self.assertEqual(self.feedback_engine.train(), True)

    def test_predict_alert(self):
        """
        Check if anomaly is correctly predicted.
        """
        self.add_anomalies()
        self.feedback_engine.train()

        anomaly_object_1 = AnomalyObject(
            self.time,
            self.ip_address,
            self.measurement_type,
            self.detection_method,
            3,
            15,
            self.asn.value
            )

        anomaly_object_2 = AnomalyObject(
            self.time,
            self.ip_address,
            self.measurement_type,
            self.detection_method,
            80,
            90,
            self.asn.value
            )
        self.assertEqual(self.feedback_engine._predict(anomaly_object_1), False)
        self.assertEqual(self.feedback_engine._predict(anomaly_object_2), True)

    def test_process_anomaly(self):
        """
        Test if anomalies are processed and stored correctly.
        """
        self.feedback_engine.train()

        anomaly_object_1 = AnomalyObject(
            self.time,
            self.ip_address,
            self.measurement_type,
            self.detection_method,
            3,
            15,
            self.asn.value
        )
        self.assertEqual(self.feedback_engine.process_anomaly(anomaly_object_1), True)
        self.assertEqual(len(Anomaly.objects.all()), 1)
        
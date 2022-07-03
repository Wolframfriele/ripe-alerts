import os
import importlib
import pandas as pd
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from database.models import Anomaly, Setting
from database.models import DetectionMethod as DetecionMethodModel
from anomaly_detection_reworked.anomaly_object import AnomalyObject
from anomaly_detection_reworked.detection_method import DetectionMethod
from anomaly_detection_reworked.detection_methods.entry_point_delay import EntryPointDelay
from ripe_interface.api import set_autonomous_system_setting
from ripe_interface.api_schemas import ASNumber

class TestAnomalyObject(TestCase):
    """Test module for the AnomalyObject."""
    def setUp(self) -> None:
        """Set up a user with autonomous system number to be able to test models, and add detection methods to database"""
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        setting = Setting.objects.create(user=user)
        self.asn = ASNumber()
        self.asn.value = 3333
        set_autonomous_system_setting(request=None, asn=self.asn)

        detection_method_class = EntryPointDelay()

        DetecionMethodModel.objects.create(
            type=detection_method_class.describe["type"],
            description=detection_method_class.describe["description"]
        )

        self.detection_method = DetecionMethodModel.objects.get(id=1)

        self.time = timezone.now()
        self.time_formatted = str(self.time.year) + "-" + str(self.time.month) + "-" + str(self.time.day) + \
                              " " + str(self.time.hour) + ":" + str(self.time.minute) + ":" + str(self.time.second)
        self.anomaly_1 = AnomalyObject(
            time=self.time_formatted,
            ip_address="198.1.2.68",
            measurement_type="traceroute",
            detection_method=self.detection_method,
            mean_increase=2,
            anomaly_score=30,
            asn="1103"
        )
        self.expected_df = pd.DataFrame({
            "ip_address": "198.1.2.68",
            "measurement_type": "traceroute",
            "detection_method": self.detection_method.type,
            "mean_increase": 2,
            "anomaly_score": 30,
            "asn": "1103"
        }, index=[0])
        return super().setUp()

    def test_get_df(self):
        """
        Check if the get df method returns the correct dataframe.
        """
        get_df = self.anomaly_1.get_df()
        assert self.expected_df.equals(get_df)
        

    def test_update_predict(self):
        self.anomaly_1.update_predict(True)
        assert self.anomaly_1.prediction_value == True

    def test_store_anomaly(self):
        assert len(Anomaly.objects.all()) == 0
        self.anomaly_1.update_predict(True)
        self.anomaly_1.store()
        assert len(Anomaly.objects.all()) == 1


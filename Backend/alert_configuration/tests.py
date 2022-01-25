from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import User, AlertConfiguration, Anomaly
from ripe_atlas.models import Measurement, Asn, Anchor
from .services import get_alerts, get_anomalies
import time


class TestAnomalies(TestCase):

    @classmethod
    def setUpTestData(cls):
        """ Fill the test database """
        cls.user = User.objects.create(username="tientjie", email="sebastiaan.cales@student.hu.nl", password="admin")
        cls.asn = Asn.objects.create(asn=1002)
        cls.anchor = Anchor.objects.create(asn=cls.asn, anchor_id=69)
        cls.measurement = Measurement.objects.create(measurement_id=69, type=Measurement.MeasurementType.PING,
                                                     interval=900, anchor=cls.anchor)
        cls.config = {"configuratie_stuff": 1}
        cls.alert_configuration = AlertConfiguration.objects.create(user=cls.user, measurement=cls.measurement,
                                                                    alert_configuration_type="ping",
                                                                    alert_configuration=
                                                                    cls.config)

        # time.sleep is used because the order of saving the anomaly in the database is wrong somehow if we dont.
        cls.anomaly_1 = Anomaly.objects.create(alert_configuration=cls.alert_configuration, description="oops", )
        time.sleep(1)
        cls.anomaly_2 = Anomaly.objects.create(alert_configuration=cls.alert_configuration, description="ohno",
                                           is_alert=True)
        time.sleep(1)
        cls.anomaly_3 = Anomaly.objects.create(alert_configuration=cls.alert_configuration, description="ohno2",
                                           is_alert=True)

    def test_get_anomalies(self):
        """anomalies should be in descending order"""
        anomalies = get_anomalies(self.user.id, 0)
        self.assertQuerysetEqual(anomalies, [self.anomaly_3, self.anomaly_2, self.anomaly_1])

    def test_get_alerts(self):
        """alerts should be in descending order"""
        alerts = get_alerts(self.user.id, 0)
        self.assertQuerysetEqual(alerts, [self.anomaly_3, self.anomaly_2])

    def test_pagination(self):
        anomalies = get_anomalies(self.user.id, 1)
        self.assertEqual(len(anomalies), 2)
        self.assertQuerysetEqual(anomalies, [self.anomaly_2, self.anomaly_1])

    def test_label_api_non_existing_anomaly(self):
        url = reverse("label-alert")
        data = {'anomaly_id': 9, 'label': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_label_api_existing_anomaly(self):
        url = reverse("label-alert")
        data = {'anomaly_id': 1, 'label': True}
        response = self.client.post(url, data, format='json')
        updated_anomaly = Anomaly.objects.get(pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_anomaly.label, True)

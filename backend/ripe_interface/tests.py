import random

import requests
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from database.models import Setting
from ripe_interface.anchor import Anchor
from ripe_interface.requests import ANCHORS_URL, RipeRequests


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


class APITest(TestCase):
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

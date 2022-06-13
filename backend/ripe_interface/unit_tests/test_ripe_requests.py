import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone

from ripe_interface.ripe_requests import RipeRequests


class RipeRequestTest(TestCase):
    """ Test module for the following RipeRequests functions:
        get_anchors(), autonomous_system_exist(), get_anchoring_measurements() """

    def setUp(self):
        self.invalid_asn = 0  # This will always be an invalid Autonomous System Number.
        self.valid_asn = 1103  # A valid ASN with multiple anchors.
        self.invalid_target_address = "194.171.96.34"  # Target address of ASN1104 (which consists of probes only)
        self.valid_target_address = "195.169.125.10"  # Target address of ASN1103

    def test_get_anchors_fail(self):
        """ Retrieves all anchors from an autonomous system (ASN0) that does not exist. """
        total_anchors = len(RipeRequests.get_anchors(self.invalid_asn))
        self.assertEqual(total_anchors, 0)

    def test_get_anchors_success(self):
        """ Retrieves all anchors from a valid autonomous system (ASN1103) that has anchors. """
        anchors = RipeRequests.get_anchors(self.valid_asn)
        total_anchors = len(anchors)
        self.assertNotEquals(total_anchors, 0)

    def test_autonomous_system_exist(self):
        """ Asserts whether an autonomous system exists or not. A valid autonomous system should return true and an
            invalid autonomous system should return false."""
        self.assertEqual(RipeRequests.autonomous_system_exist(self.invalid_asn), False)
        self.assertEqual(RipeRequests.autonomous_system_exist(self.valid_asn), True)

    def test_get_anchoring_measurements_fail(self):
        """ Retrieves the latest anchoring measurement data with invalid target address.
            This should return zero measurements."""
        total_measurements = len(RipeRequests.get_anchoring_measurements(self.invalid_target_address))
        self.assertEqual(total_measurements, 0)

    def test_get_anchoring_measurements_success(self):
        """ Retrieves the latest anchoring measurement data with valid target address.
            This should return at least 1 measurement."""
        total_measurements = len(RipeRequests.get_anchoring_measurements(self.valid_target_address))
        self.assertNotEquals(total_measurements, 0)

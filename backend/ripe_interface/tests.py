import random

import requests
from django.test import TestCase, Client
from django.urls import reverse

# Valid ASN:12770, ASN:29432
from ripe_interface.anchor import Anchor
from ripe_interface.requests import ANCHORS_URL, RipeRequests


class RipeRequestTest(TestCase):

    def setUp(self):
        self.invalid_asn = 0   # This will always be an invalid Autonomous System Number.
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

class GetSingleASTest(TestCase):
    """ Test module for GET single puppy API """

    # def test_get_random_autonomous_system(self):  # -> list[Anchor]:
    #     """Returns a list of random currently online anchors """
    #     random_id = random.randint(1, 30)
    #     # print(random_id)
    #     response = requests.get(url=ANCHORS_URL + "10").json()
    #     anchor = Anchor(**response)
    #     print(anchor)
    #     self.assertEqual(1, 1)
    #
    # def test_set_asn_endpoint(self):
    #     self.assertEqual(1, 1)

    # client = Client()

    # def setUp(self):
    #     return
    # self.casper = Puppy.objects.create(
    #     name='Casper', age=3, breed='Bull Dog', color='Black')
    # self.muffin = Puppy.objects.create(
    #     name='Muffin', age=1, breed='Gradane', color='Brown')
    # self.rambo = Puppy.objects.create(
    #     name='Rambo', age=2, breed='Labrador', color='Black')
    # self.ricky = Puppy.objects.create(
    #     name='Ricky', age=6, breed='Labrador', color='Brown')

    def test_get_valid_single_puppy(self):
        response = self.client.get('/api/asn/')

        print(response.context)
        print(response.content)
        print(response.json()['id'])
        # puppy = Puppy.objects.get(pk=self.rambo.pk)
        # serializer = PuppySerializer(puppy)
        self.assertEqual(1, 1)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data, serializer.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_invalid_single_puppy(self):
    #     response = client.get(
    #         reverse('get_delete_update_puppy', kwargs={'pk': 30}))
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

import random

import requests
from django.test import TestCase, Client
from django.urls import reverse

# Valid ASN:12770, ASN:29432
from ripe_interface.anchor import Anchor
from ripe_interface.requests import ANCHORS_URL


class ASTestCase(TestCase):
    lion = 1
    cat = 22
    client = Client()

    def setUp(self):
        self.cat = 223  # cat is now another number

    def test_animals_can_speak(self):
        """Autonomous systems that can be added or deleted"""
        self.assertNotEquals(self.lion, 12)
        self.assertNotEquals(self.cat, 22)

    def test_get_random_autonomous_system(self):  # -> list[Anchor]:
        """Returns a list of random currently online anchors """
        random_id = random.randint(1, 30)
        print(random_id)
        response = requests.get(url=ANCHORS_URL + "10").json()
        anchor = Anchor(**response)


        self.assertEqual(1, 1)


class GetSingleASTest(TestCase):
    """ Test module for GET single puppy API """

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

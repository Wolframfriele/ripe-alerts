from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from ripe_atlas.models import Measurement, Asn, Anchor
from .models import RipeUser
from django.contrib.auth.models import User


class TestInitialSetup(TestCase):

    @classmethod
    def setUpTestData(cls):
        """ Fill the test database """
        user = User.objects.create(username="tientjie", email="sebastiaan.cales@student.hu.nl", password="admin")
        RipeUser.objects.create(user=user, ripe_api_token="992ef48b-babc-4885-932e-429bc9277b41")

    def test_store_initial_setup_asn_not_found(self):
        url = reverse('initial-setup')
        data = {'asns': [0], 'email': 'example.email.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_store_initial_setup_anchor_found(self):
        mock_response_patcher = patch('ripe_atlas.interfaces.requests.post')
        mock_response = mock_response_patcher.start()
        mock_response.return_value = None
        url = reverse('initial-setup')
        data = {'asns': [208800], 'email': 'example.email.com'}
        response = self.client.post(url, data, format='json')
        user = User.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asn.objects.count(), 1)
        self.assertEqual(Anchor.objects.count(), 1)
        self.assertEqual(Measurement.objects.count(), 4)
        self.assertEqual(user.ripe_user.initial_setup_complete, True)





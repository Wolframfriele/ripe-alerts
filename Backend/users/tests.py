from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ripe_atlas.models import Measurement, Asn, Anchor


class TestInitialSetup(APITestCase):

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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asn.objects.count(), 1)
        self.assertEqual(Anchor.objects.count(), 1)
        self.assertEqual(Measurement.objects.count(), 4)






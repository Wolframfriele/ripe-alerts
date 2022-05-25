from django.contrib.auth.models import User
from django.test import TestCase, Client

from database.models import Setting
from ripe_interface.api import set_autonomous_system_setting
from ripe_interface.api_schemas import ASNumber


class APITestSetAutonomousSystemSetting(TestCase):
    """ Test module for PUT api/settings/{asn_number} endpoint. """

    def setUp(self):
        """ In order to test this endpoint, we'll
            first have to create a user and a user configuration. """
        self.client = None
        self.valid_asn = 1103
        self.invalid_asn = 1
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        Setting.objects.create(user=user)

    def test_set_autonomous_system_setting_success(self):
        """ User has been configured, time to use/test the endpoint with a valid autonomous system number. """
        self.client = Client()
        response = self.client.put('/api/settings/' + str(self.valid_asn))
        result = response.json()
        monitoring_possible = result.get('monitoring_possible')
        host_is_empty = not bool(result.get('host'))
        message = result.get('message')
        self.assertEqual(monitoring_possible, True)
        self.assertEqual(host_is_empty, False)
        self.assertEqual(message, "Success!")
        self.assertEqual(response.status_code, 200)

    def test_set_autonomous_system_setting_fail(self):
        """ User is still configured, now we will use/test the endpoint with an invalid autonomous system number. """
        self.client = Client()  # Reset session and cookies from the client.
        response = self.client.put('/api/settings/' + str(self.invalid_asn))
        result = response.json()
        monitoring_possible = result.get('monitoring_possible')
        host = result.get('host')
        message = result.get('message')
        self.assertEqual(monitoring_possible, False)
        self.assertEqual(host, None)
        self.assertIn("ASN", message)
        self.assertIn("does not exist!", message)
        self.assertEquals(response.status_code, 404)


class APITestGetAutonomousSystemSettingSuccess(TestCase):
    """ Test module 1/2 for GET api/settings/ endpoint. """

    def setUp(self):
        """ In order to test this endpoint, we'll
            first have to create a user and a user configuration with a configured autonomous system number. """
        self.client = Client()
        self.valid_asn = 1103  # ASN1103 is owned by SURFNET-NL - SURF B.V.
        self.invalid_asn = 1
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        Setting.objects.create(user=user)
        self.asn = ASNumber()
        self.asn.value = self.valid_asn
        set_autonomous_system_setting(request=None, asn=self.asn)

    def test_get_autonomous_system_setting_success(self):
        """ Get the autonomous system settings of the user and verify the json attributes. """
        response = self.client.get('/api/settings/')
        result = response.json()
        monitoring_possible = result.get('monitoring_possible')
        host = result.get('host')
        message = result.get('message')
        autonomous_system = result.get('autonomous_system')
        self.assertEquals(response.status_code, 200)
        self.assertEqual(monitoring_possible, True)
        self.assertEqual(host, 'SURFNET-NL - SURF B.V.')
        self.assertEqual(message, 'Success!')
        self.assertEqual(autonomous_system, 'ASN1103')


class APITestGetAutonomousSystemSettingFail(TestCase):
    """ Test module 2/2 for GET api/settings/ endpoint. """

    def setUp(self):
        """ In order for this endpoint to fail, we'll
            first have to create a user without an autonomous system configuration. """
        self.client = Client()
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        Setting.objects.create(user=user)

    def test_get_autonomous_system_setting_fail(self):
        """ Get the autonomous system settings of the user and verify the json attributes. """
        response = self.client.get('/api/settings/')
        result = response.json()
        monitoring_possible = result.get('monitoring_possible')
        host = result.get('host')
        message = result.get('message')
        autonomous_system = result.get('autonomous_system')
        self.assertEquals(response.status_code, 404)
        self.assertEqual(monitoring_possible, False)
        self.assertEqual(host, None)
        self.assertEqual(message, 'ASN configuration not found!')
        self.assertEqual(autonomous_system, None)

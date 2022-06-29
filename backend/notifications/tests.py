import json
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase


from database.models import Setting, Notification
from .api_schema import AlertFormat, ConfigFormat, ConfigFormatGet
from .api import send_alert, setup, save_config, get_config




class AlertApiTest(TestCase):
    """ Test for the alert API """

    def setUp(self):
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        setting = Setting.objects.create(user=user)
        notifications = Notification.objects.create(setting=setting, name="Webhook", config="""{"description":"This a plugin to send message by using webhooks", 
                    "url":"http://localhost:8000/"}""")
        setup()

        self.alert = AlertFormat(alert="A anomaly was detected!")
        self.response = send_alert(request=None, data=self.alert)
        self.json_response = json.loads(self.response.content)

        self.bad_alert = AlertFormat()
        self.bad_response = send_alert(request=None, data=self.bad_alert)
        self.bad_json_response = json.loads(self.bad_response.content)


    def test_response_valid(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.json_response['message'], "Succesfully send the alert!")

    def test_response_invalid(self):
        self.assertEqual(self.bad_response.status_code, 400)
        self.assertEqual(self.bad_json_response['message'], "Missing parameter!")

class ConfigSaveTest(TestCase):
    """ Test for the saving of the config """

    def setUp(self):
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        setting = Setting.objects.create(user=user)
        
        setup()
        
        config_data = {"description":"This a plugin to send message by using webhooks", 
                    "url":"http://localhost:8000/"}

        self.config = ConfigFormat(name="Webhook", config=json.dumps(config_data))
        self.response = save_config(request=None, data=self.config)
        self.json_response = json.loads(self.response.content)

        self.bad_config = ConfigFormat(name='test', config= '')
        self.bad_response = save_config(request=None, data=self.bad_config)
        self.bad_json_response = json.loads(self.bad_response.content)

    def test_response_valid(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.json_response['message'], "The plugin has been succesfully saved!")
        self.assertTrue(Notification.objects.filter(name="Webhook").exists())

    def test_response_invalid(self):
        self.assertEqual(self.bad_response.status_code, 400)
        self.assertEqual(self.bad_json_response['message'], "Invalid parameters!")
        self.assertFalse(Notification.objects.filter(name="test").exists())

class ConfigGetTest(TestCase):
    """ Test for getting the saves from the database """

    def setUp(self):
        user = User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
        setting = Setting.objects.create(user=user)
        config = {"description":"This a plugin to send message by using webhooks", 
                    "url":"http://localhost:8000/"}
        Notification.objects.create(setting=setting, name="Webhook", config=config)
        Notification.objects.create(setting=setting, name="print_plugin", config=config)
        
        setup()
        
        self.get_one_config = ConfigFormatGet(plugin="Webhook")
        self.response = get_config(request=None, data=self.get_one_config)
        self.json_response = json.loads(self.response.content)

        self.get_all_config = ConfigFormatGet(plugin="all")
        self.response_all = get_config(request=None, data=self.get_all_config)
        self.json_response_all = json.loads(self.response.content)

        self.bad_config = ConfigFormatGet(name='')
        self.bad_response = get_config(request=None, data=self.bad_config)
        self.bad_json_response = json.loads(self.bad_response.content)

    def test_get_one(self):
        self.assertEqual(self.response.status_code, 200)

    def test_get_all(self):
        self.assertEqual(self.response_all.status_code, 200)
        
    def test_response_invalid(self):
        self.assertEqual(self.bad_response.status_code, 400)
        self.assertEqual(self.bad_json_response['message'], "Missing parameter!")
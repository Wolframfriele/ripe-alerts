# from django.test import TestCase
# from unittest.mock import patch
# from services import InitialSetupService
# from apis import InitialSetup
#
# # Create your tests here.
# class TestInitialSetupService(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.mock_response_patcher = patch('ripe_atlas.interfaces.requests.get')
#         cls.mock_response = cls.mock_response_patcher.start()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.mock_response_patcher.stop()
#
#     def test_store_initial_setup(self):
#         validated_data = {'anchors_by_asn': {}, 'email': "sebastiaan.cales@student.hu.nl"}
#
#
#

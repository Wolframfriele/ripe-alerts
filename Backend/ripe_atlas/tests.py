from django.test import TestCase
from unittest.mock import patch
from ripe_atlas.interfaces import RipeInterface
from collections import defaultdict

"""Integration tests Ripe Atlas"""


class MockResponse:

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestRipeInterface(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_response_patcher = patch('ripe_atlas.interfaces.requests.get')
        cls.mock_response = cls.mock_response_patcher.start()
        cls.valid_token = "115c25fc-8815-4710-9865-85d49dc4778a"
        cls.invalid_token = ""

    @classmethod
    def tearDownClass(cls):
        cls.mock_response_patcher.stop()

    """
    When we send a request to Ripe Atlas and we use a ripe_api_token, when the token is invalid we
    get a 403 status code and if token is valid we get a 200 status code
    """

    def test_is_token_valid_when_valid(self):
        self.mock_response.return_value = MockResponse("OK", 200)
        valid = RipeInterface.is_token_valid(self.valid_token)
        self.assertTrue(valid)

    def test_is_token_valid_when_invalid(self):
        self.mock_response.return_value = MockResponse(
            {"error": {"detail": "The provided API key does not exist"}}, 403)
        invalid = RipeInterface.is_token_valid(self.invalid_token)
        self.assertFalse(invalid)

    def test_get_anchoring_measurements_no_results(self):
        self.mock_response.return_value = MockResponse({"results": []}, 200)
        measurements = RipeInterface.get_anchoring_measurements("159.89.173.104")
        self.assertEqual(measurements, [])

    def test_get_anchoring_measurements_with_results(self):
        results = {"results": [
            {
                "description": "Anchoring Mesh Measurement: Traceroute IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207652,
                "interval": 900,
                "type": "traceroute"
            },
            {
                "description": "Anchoring Mesh Measurement: Ping IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207653,
                "interval": 240,
                "type": "ping"
            },
            {
                "description": "Anchoring Mesh Measurement: Http IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207654,
                "interval": 1800,
                "type": "http",
            },
            {
                "description": "Anchoring Probes Measurement: Traceroute IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207978,
                "interval": 900,
                "type": "traceroute"
            },
            {
                "description": "Anchoring Probes Measurement: Ping IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207979,
                "interval": 240,
                "type": "ping"
            },
            {
                "description": "Anchoring Probes Measurement: Http IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207980,
                "interval": 1800,
                "type": "http",
            }
        ]}
        self.mock_response.return_value = MockResponse(results, 200)
        measurements = RipeInterface.get_anchoring_measurements("149.89.173.104")

        expected_processed_results = [
            {
                "description": "Anchoring Mesh Measurement: Traceroute IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207652,
                "interval": 900,
                "type": "traceroute"
            },
            {
                "description": "Anchoring Mesh Measurement: Ping IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207653,
                "interval": 240,
                "type": "ping"
            },
            {
                "description": "Anchoring Probes Measurement: Traceroute IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207978,
                "interval": 900,
                "type": "traceroute"
            },
            {
                "description": "Anchoring Probes Measurement: Ping IPv6 for anchor ae-dxb-as15802.anchors.atlas.ripe.net",
                "id": 19207979,
                "interval": 240,
                "type": "ping"
            },
        ]
        self.assertEqual(expected_processed_results, measurements)

    def test_get_anchors(self):
        asn_list = [12, 208800, 15412]
        json_1 = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []}
        json_2 = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 2182,
                    "type": "Anchor",
                    "fqdn": "ae-auh-as208800.anchors.atlas.ripe.net",
                    "probe": 6771,
                    "is_ipv4_only": True,
                    "ip_v4": "91.201.7.243",
                    "as_v4": 208800,
                    "ip_v4_gateway": None,
                    "ip_v4_netmask": None,
                    "ip_v6": None,
                    "as_v6": None,
                    "ip_v6_gateway": None,
                    "ip_v6_prefix": None,
                    "city": "Abu Dhabi",
                    "country": "AE",
                    "company": "EOS CLOUD TECHNOLOGY L.L.C.",
                    "nic_handle": "",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            54.3773438,
                            24.453884
                        ]
                    },
                    "tlsa_record": "",
                    "is_disabled": False,
                    "date_live": "2020-04-16T14:20:00.410044",
                    "hardware_version": 99
                }
            ]
        }
        json_3 = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 2825,
                    "type": "Anchor",
                    "fqdn": "ae-dxb-as15412-client.anchors.atlas.ripe.net",
                    "probe": 7047,
                    "is_ipv4_only": False,
                    "ip_v4": "80.77.4.60",
                    "as_v4": 15412,
                    "ip_v4_gateway": None,
                    "ip_v4_netmask": None,
                    "ip_v6": "2001:1a00:acca:130d::4",
                    "as_v6": 15412,
                    "ip_v6_gateway": None,
                    "ip_v6_prefix": None,
                    "city": "Dubai",
                    "country": "AE",
                    "company": "Emirates Integrated Telecommunications Company PJSC",
                    "nic_handle": "EITC4-RIPE",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            55.1868599,
                            25.0264601
                        ]
                    },
                    "tlsa_record": "",
                    "is_disabled": False,
                    "date_live": "2021-12-14T18:20:00.494487",
                    "hardware_version": 99
                }
            ]
        }
        result_1 = MockResponse(json_1, 200)
        result_2 = MockResponse(json_2, 200)
        result_3 = MockResponse(json_3, 200)

        self.mock_response.side_effect = [result_1, result_2, result_3]
        expected_result = defaultdict(list)
        expected_result[208800].extend(json_2['results'])
        expected_result[15412].extend(json_3['results'])
        result = RipeInterface.get_anchors(asn_list)
        self.assertEqual(expected_result, result)
        self.mock_response.side_effect = None

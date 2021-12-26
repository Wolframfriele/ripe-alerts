from django.test import TestCase
from interfaces import RipeInterface
"""Integration tests Ripe Atlas"""


class FirstTest(TestCase):
    def test_hello_world(self):
        text = "hello world!"
        self.assertEqual(text, "hello world!")


class TestRipeInterface(TestCase):
    pass
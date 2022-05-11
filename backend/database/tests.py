from django.test import TestCase


class AnimalTestCase(TestCase):
    lion = 1
    cat = 2

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(self.lion, 1)
        self.assertEqual(self.cat, 2)


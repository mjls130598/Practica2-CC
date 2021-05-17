from django.test import TestCase
from django.urls import reverse

class PrediccionTest(TestCase):
    def testVersion1(self):
        response = self.client.get(reverse('version1', args=[24]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.content, "")

    def testVersion2(self):
        response = self.client.get(reverse('version2', args=[24]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.content, "")

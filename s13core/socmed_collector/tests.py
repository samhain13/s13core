from django.core.exceptions import FieldError
from django.test import TestCase

from .models import APIKey


class SocMedCollectorTests(TestCase):

    def test_apikey_label_unique(self):
        label = 'Social Media Key'
        api_key0 = APIKey(
            key='123456789A',
            label=label
        )
        api_key0.save()
        label = 'social media key'
        api_key1 = APIKey(
            key='123456789B',
            label=label
        )
        self.assertRaises(FieldError, api_key1.save)

    def test_apikey_str_method(self):
        label = 'Social Media Key'
        api_key = APIKey(
            key='123456789A',
            label=label
        )
        self.assertEqual(str(api_key), 'APIKey: {}'.format(label))
